import socket
import subprocess
import time
from collections.abc import Generator

from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic

from qurix.kafka.entities.config import (AdminConfig, ConsumerConfig, Offset)

TEST_TOPIC_NAME = "example_topic"
BOOTSTRAP_SERVERS = "localhost:9092"

TEST_TOPIC_NAME = "example_topic"
BOOTSTRAP_SERVERS = "localhost:9092"

consumer_config = ConsumerConfig(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    group_id="my_consumer_group",
    auto_offset_reset=Offset.EARLIEST.value
)

admin_config = AdminConfig(
    bootstrap_servers=BOOTSTRAP_SERVERS
)


def tearup(wait_seconds: int = 10) -> Generator[str]:
    tearup_script = "tests/scripts/tearup.sh"
    subprocess.call(["chmod", "+x", tearup_script])
    subprocess.call(tearup_script, shell=True)
    time.sleep(wait_seconds)
    base_conf = {
        "bootstrap.servers": BOOTSTRAP_SERVERS
    }
    admin_client = AdminClient(base_conf)
    topic_list = []
    topic_list.append(NewTopic(TEST_TOPIC_NAME, 1, 1))
    admin_client.create_topics(topic_list)
    producer_conf = {**base_conf, 'client.id': socket.gethostname()}

    producer = Producer(producer_conf)
    producer.poll(5)
    producer.produce(TEST_TOPIC_NAME, '{"some": "message"}'.encode(
        'utf-8'))
    producer.flush()


def teardown(wait_seconds: int = 10) -> Generator[str]:
    teardown_script = "tests/scripts/teardown.sh"
    subprocess.call(["chmod", "+x", teardown_script])
    subprocess.call(teardown_script, shell=True)
    time.sleep(wait_seconds)
    yield "finished"
