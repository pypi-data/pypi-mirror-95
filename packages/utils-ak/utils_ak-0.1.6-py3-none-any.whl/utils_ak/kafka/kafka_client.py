# from confluent_kafka import Producer, Consumer
import uuid

from utils_ak.builtin import update_dic
from copy import deepcopy

# todo: make group_id properly

DEFAULT_CONSUMER_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': str(uuid.uuid4()),
    'default.topic.config': {
        'auto.offset.reset': 'largest'
    },
    'enable.auto.commit': False,
    'enable.partition.eof': False,
}

DEFAULT_PRODUCER_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'queue.buffering.max.ms': 1,
    'queue.buffering.max.messages': 1000000,
    'max.in.flight.requests.per.connection': 1,
    'default.topic.config': {'acks': 'all'}
}


class KafkaClient:
    def __init__(self, consumer_config=None, producer_config=None):
        self.kafka_topics = []

        consumer_config = consumer_config or {}
        self.consumer_config = deepcopy(DEFAULT_CONSUMER_CONFIG)
        self.consumer_config = update_dic(self.consumer_config, consumer_config)
        self.consumer = Consumer(self.consumer_config)

        producer_config = producer_config or {}
        self.producer_config = deepcopy(DEFAULT_PRODUCER_CONFIG)
        self.producer_config = update_dic(self.producer_config, producer_config)
        self.producer = Producer(self.producer_config)

        self.init_subscriptions = False

    def subscribe(self, topic):
        if topic not in self.kafka_topics:
            self.kafka_topics.append(topic)
            # self.consumer.subscribe(self.kafka_topics)

    def publish(self, topic, msg):
        self.producer.produce(topic, msg)
        self.producer.poll(0)

    def poll(self, timeout=0.):
        self.start_listening()
        return self.consumer.poll(timeout)

    def start_listening(self):
        if not self.init_subscriptions:
            self.consumer.subscribe(self.kafka_topics)
            self.init_subscriptions = True


if __name__ == '__main__':
    cli = KafkaClient(consumer_config={'default.topic.config': {
        'auto.offset.reset': 'smallest'
    }})
    cli.subscribe('binance_trades')

    i = 0
    while True:
        msg = cli.poll()
        if not msg:
            continue
        print(msg, msg.offset(), msg.value())
        print(i)

        i += 1
