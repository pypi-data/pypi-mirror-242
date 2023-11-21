from collections.abc import Generator

import pandas as pd
import pytest
from confluent_kafka import Consumer

from qurix.kafka.observer import KafkaObserver
from tests.common import consumer_config, teardown, tearup


@pytest.fixture
def kafka_observer() -> Generator[KafkaObserver]:
    tearup(5)
    yield KafkaObserver(consumer_config)
    teardown(5)


@pytest.mark.integration_test
def test_get_consumer_config(kafka_observer: KafkaObserver):
    consumer_config = kafka_observer.consumer_config
    consumer_config_dict = consumer_config.to_dict()
    assert "group.id" in consumer_config_dict
    assert "auto.offset.reset" in consumer_config_dict


@pytest.mark.integration_test
def test_get_topic_info(kafka_observer: KafkaObserver):
    result = kafka_observer.get_topic_info()
    assert len(result) > 0


@pytest.mark.integration_test
def test_get_topic_info_extended(kafka_observer: KafkaObserver):
    result = kafka_observer.get_topic_info(extended=True)
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    expected_columns = ["topic_name", "partition", "replication_factor", "commited_offset",
                        "current_offset", "calculated_offset", "low_watermark",
                        "high_watermark", "retention_time", "retention_size", "cleanup_policy"]
    assert all([col in result.columns for col in expected_columns])


@pytest.mark.integration_test
def test_get_consumer_groups(kafka_observer: KafkaObserver):
    result = kafka_observer.get_consumer_groups()
    group_id_key = "group_id"
    assert len(result) > 0
    assert result[group_id_key] is not None


@pytest.mark.integration_test
def test_get_consumer_group_offsets(kafka_observer: KafkaObserver):
    result = kafka_observer.get_consumer_group_offsets(
        group_id="my_consumer_group")
    assert len(result) > 0
    assert result["group_id"][0] == "my_consumer_group"
    assert result["topic_name"][0] == "example_topic"


@pytest.mark.integration_test
def test_get_consumer_groups_offsets(kafka_observer: KafkaObserver):
    result = kafka_observer.get_consumer_groups_offsets()
    assert len(result) > 0


@pytest.mark.integration_test
def test_observer_offset_plot(kafka_observer: KafkaObserver):
    consumer = Consumer(kafka_observer.consumer_config.to_dict())
    kafka_observer.plot_offset_status(consumer, "example_topic")
