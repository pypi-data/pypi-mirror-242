import pandas as pd
import pytest

from qurix.kafka.entities.base import BaseEntity
from qurix.kafka.entities.observer_metrics import TopicInfo


@pytest.fixture
def topic_info_sample() -> TopicInfo:
    return TopicInfo(topic_name="some_topic",
                     partition=0,
                     replication_factor=1)


@pytest.fixture
def second_topic() -> TopicInfo:
    return TopicInfo(topic_name="second_topic",
                     partition=0,
                     replication_factor=1)


def test_topic_info(topic_info_sample: TopicInfo):
    assert isinstance(topic_info_sample, BaseEntity)
    assert topic_info_sample.topic_name == "some_topic"
    assert topic_info_sample.partition == 0

    result_dict = topic_info_sample.to_dict()
    assert result_dict["topic_name"] == "some_topic"


def test_one_topic_info_df(topic_info_sample: TopicInfo):
    result_df = pd.DataFrame([topic_info_sample])
    assert result_df["topic_name"].tolist() == ["some_topic"]


def test_many_topics_df(topic_info_sample: TopicInfo, second_topic: TopicInfo):
    topic_list = [topic_info_sample, second_topic]
    topic_list_as_dict = [x.to_dict() for x in topic_list]

    result_df_list = pd.DataFrame(topic_list_as_dict)
    assert result_df_list["topic_name"].tolist() == [
        "some_topic", "second_topic"]
