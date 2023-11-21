from dataclasses import dataclass

from qurix.kafka.entities.base import BaseEntity


@dataclass(frozen=True)
class TopicInfo(BaseEntity):
    topic_name: str
    partition: int
    replication_factor: int


@dataclass(frozen=True)
class WatermarkInfo(BaseEntity):
    topic_name: str
    partition: int
    commited_offset: int
    current_offset: int
    calculated_offset: int
    low_watermark: int
    high_watermark: int


@dataclass(frozen=True)
class ConsumerData(BaseEntity):
    topic_name: str
    partition: int
    commited_offset: int
    current_offset: int
    calculated_offset: int
    low_watermark: int
    high_watermark: int


@dataclass(frozen=True)
class RetentionPolicyInfo(BaseEntity):
    topic_name: str
    retention_time: list[int]
    retention_size: list[str]
    cleanup_policy: list[str]


@dataclass(frozen=True)
class ConsumerGroup(BaseEntity):
    group_id: str


@dataclass(frozen=True)
class ConsumerGroupsOffset(BaseEntity):
    group_id: str
    topic_name: str
    partition: int
    offset: int
