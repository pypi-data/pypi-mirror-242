from dataclasses import dataclass

import pytest

from qurix.kafka.entities.config import (BaseConfig, ConsumerConfig, Offset)


@pytest.fixture
def sample_class_instance() -> BaseConfig:
    @dataclass
    class SomeClass(BaseConfig):
        a_second_property: str
        b_second_property: str

    return SomeClass("a", "b")


@pytest.fixture
def consumer_config() -> ConsumerConfig:
    return ConsumerConfig(bootstrap_servers="localhost:9092",
                          group_id="group_1")


def test_base_config(sample_class_instance: BaseConfig):
    result = sample_class_instance.to_dict(remove_none_values=False)
    assert "a.second.property" in result
    assert "b.second.property" in result


def test_consumer_config(consumer_config: ConsumerConfig):
    result = consumer_config.to_dict(remove_none_values=False)
    expected_keys = ["bootstrap.servers",
                     "group.id",
                     "auto.offset.reset",
                     "enable.auto.commit",
                     "security.protocol",
                     "sasl.mechanisms",
                     "sasl.username",
                     "sasl.password"]
    assert all([key in result for key in expected_keys])


def test_offset_values():
    assert Offset.EARLIEST.value == "earliest"
    assert Offset.LATEST.value == "latest"
    assert Offset.LAST.value == "last"
    assert Offset.TIMESTAMP.value == "timestamp"
    assert Offset.EXPLICIT.value == "explicit"
