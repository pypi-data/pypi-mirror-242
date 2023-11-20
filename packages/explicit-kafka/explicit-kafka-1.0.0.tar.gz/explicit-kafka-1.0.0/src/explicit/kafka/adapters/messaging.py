"""Реализация адаптера обмена сообщениями."""
from typing import Dict
from typing import Generator
from typing import Optional
import logging

from confluent_kafka import Consumer as Subscriber
from confluent_kafka import KafkaError
from confluent_kafka import KafkaException
from confluent_kafka import Message as KafkaMessage
from confluent_kafka import Producer as Publisher
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic
from pydantic.fields import Field
from pydantic.main import BaseModel

from explicit.adapters.messaging import AbstractAdapter


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def publish_callback(error, message: KafkaMessage):
    if error is not None:
        logger.error('Ошибка при публикации сообщения: %s', error)
    else:
        logger.info('Сообщение доставлено: %s [%s]', message.topic(), message.partition())
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Тело сообщения: %s', message.value())


class BaseConfig(BaseModel):

    bootstrap__servers: str

    class Config:
        fields = {  # Aliases
            'bootstrap__servers': 'bootstrap.servers',
        }


class PublishConfig(BaseConfig):

    class Config(BaseConfig.Config):
        fields = {
            **BaseConfig.Config.fields
        }


class SubscribeConfig(BaseConfig):

    group__id: str
    auto__offset__reset: str = Field('earliest', const=True)

    class Config(BaseConfig.Config):
        fields = {
            'auto__offset__reset': 'auto.offset.reset',
            'group__id': 'group.id',
            **BaseConfig.Config.fields
        }


class Adapter(AbstractAdapter):

    """Адаптер обмена сообщениями через Kafka."""

    def __init__(
        self, *,
        subscribe_config: Optional[SubscribeConfig] = None,
        publish_config: Optional[PublishConfig] = None,
    ) -> None:
        self._subscribe_config = subscribe_config
        self._publish_config = publish_config
        self._publisher: Publisher = None
        self._subscribers: Dict[str, Subscriber] = {}

    def _ensure_topics(self, *topics: str):
        available_config = self._publish_config or self._subscribe_config
        if available_config is None:
            raise RuntimeError('Connection is not configured')

        admin = AdminClient({'bootstrap.servers': available_config.bootstrap__servers})

        state = admin.list_topics(timeout=30.0)

        new_topics = [
            NewTopic(name, num_partitions=1) for name in topics
            if name not in state.topics
        ]

        if not new_topics:  # Все используемые топики созданы
            return

        futures = admin.create_topics(new_topics, request_timeout=30.0)
        for topic, future in futures.items():
            try:
                future.result()
            except KafkaException as e:
                error = e.args[0]
                if error.code() in ('TOPIC_ALREADY_EXISTS', ):
                    pass
            except Exception:  # pylint: disable=broad-exception-caught
                logger.exception('Невозможно создать topic')
            else:
                logger.info('Topic %s создан', topic)

    def _ensure_publisher(self):
        if self._publish_config is None:
            raise RuntimeError('Publisher is not configured')

        if self._publisher is None:
            self._publisher = Publisher(self._publish_config.dict(by_alias=True))

        return self._publisher

    def _make_subscriber_key(self, *topics: str) -> str:
        return ','.join(sorted(topics))

    def _ensure_subscriber(self, *topics: str) -> Subscriber:
        if self._subscribe_config is None:
            raise RuntimeError('Subscriber is not configured')

        key = self._make_subscriber_key(*topics)

        subscriber = self._subscribers.get(key)

        if subscriber is None:
            self._subscribers[key] = Subscriber(self._subscribe_config.dict(by_alias=True))
        return self._subscribers[key]

    def _should_continue_polling(
        self, message: KafkaMessage, break_on_eof: bool, break_on_error: bool
    ) -> Optional[bool]:
        """Продолжать ли опрос, если возникла ошибка или был достигнут конец партиции.

        :param message: Сообщение из Kafka.
        :param break_on_eof: Останавливать опрос подписчика при исчерпании сообщений.
        :param break_on_error: Останавливать опрос подписчика при ошибках.
        :return: True если нужно продолжить опрос, False нужно прекратить опрос, None действия не требуются.
        """
        eof = message is None or message.error() == KafkaError._PARTITION_EOF  # pylint: disable=protected-access
        if eof:
            return not break_on_eof
        elif error := message.error():
            logger.error('Ошибка при получении сообщения: %s', error)
            return not break_on_error
        return None

    def _poll_subscriber(
        self,
        subscriber: Subscriber,
        break_on_eof: bool = False,
        break_on_error: bool = False,
    ) -> Generator[KafkaMessage, None, None]:
        """Опрашивает подписчики и генерирует сообщения.

        :param subscriber: Набор подписчиков для опроса.
        :param break_on_eof: Останавливать опрос подписчика при исчерпании сообщений.
        :param break_on_error: Останавливать опрос подписчика при ошибках.
        :return: Генератор сообщений из Kafka.
        """

        while True:
            message: KafkaMessage = subscriber.poll(1.0)

            continue_polling = self._should_continue_polling(message, break_on_eof, break_on_error)
            if continue_polling is True:
                continue
            elif continue_polling is False:
                break

            logger.info('Получено сообщение из %s', message.topic())
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('Тело сообщения: %s', message.value())

            yield message

    def publish(self, topic: str, message: str, *args, **kwargs) -> None:
        publisher = self._ensure_publisher()

        self._ensure_topics(topic)

        publisher.poll(0)
        publisher.produce(topic, message, callback=publish_callback)
        publisher.flush()

    def subscribe(self, *topics: str) -> Generator[KafkaMessage, None, None]:
        self._ensure_topics(*topics)
        subscriber: Subscriber = self._ensure_subscriber(*topics)
        subscriber.subscribe(list(topics))
        yield from self._poll_subscriber(subscriber)
