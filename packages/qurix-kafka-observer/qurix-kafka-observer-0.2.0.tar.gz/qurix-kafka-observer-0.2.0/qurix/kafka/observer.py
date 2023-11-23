import pandas as pd
from confluent_kafka import (Consumer, ConsumerGroupTopicPartitions,
                             TopicPartition)
from confluent_kafka.admin import AdminClient, ConfigResource, TopicMetadata

from qurix.kafka.entities import base as entities_base
from qurix.kafka.entities.config import (AdminConfig, ConsumerConfig, Offset)
from qurix.kafka.entities.observer_metrics import (ConsumerGroup, ConsumerGroupsOffset, RetentionPolicyInfo, TopicInfo, WatermarkInfo)

COMMITED_OFFSET = -1001


class KafkaObserver:
    def __init__(self, config: ConsumerConfig):
        self.consumer_config = config
        admin_client_config = self._derive_admin_config(config)
        self.admin_client = AdminClient(admin_client_config.to_dict())

    @staticmethod
    def _derive_admin_config(config: ConsumerConfig) -> AdminConfig:
        relevant_keys = ["bootstrap_servers",
                         "security_protocol",
                         "sasl_mechanisms",
                         "sasl_username",
                         "sasl_password"]
        admin_config_dict = {k.replace(".", "_"): v for k, v in config.to_dict().items()
                             if k.replace(".", "_") in relevant_keys}
        return AdminConfig(**admin_config_dict)

    def get_watermark_info(self, topic: str) -> list[WatermarkInfo]:
        with Consumer(topic=topic, consumer_config=self.consumer_config) as consumer_context:
            watermark_info = self.get_offset_status(consumer_context)
        return watermark_info

    def get_retention_policy_info(self, topic: str) -> RetentionPolicyInfo:
        resource = ConfigResource("topic", topic)
        result = self.admin_client.describe_configs([resource])
        value_list = list(result.values())[0].result()
        return RetentionPolicyInfo(
            topic_name=topic,
            retention_time=[value_list["retention.ms"].value],
            retention_size=[value_list["retention.bytes"].value],
            cleanup_policy=[value_list["cleanup.policy"].value]
        )

    def get_topic_info(
        self, extended: bool = False, selected_topics: list[str] | None = None
    ) -> pd.DataFrame:
        # Get topics with self.admin_client
        topics: list[TopicMetadata] = self.admin_client.list_topics().topics

        if selected_topics is not None:
            topics: dict = {
                topic: value for topic, value in topics.items() if topic in selected_topics
            }

        topic_info_list: list[TopicInfo] = []

        for topic_name, topic in topics.items():
            for partition_id, partition in topic.partitions.items():
                topic_info_list.append(TopicInfo(topic_name=topic_name,
                                                 partition=partition_id,
                                                 replication_factor=len(partition.replicas)))

        df = entities_base.dataclass_to_df(topic_info_list)

        if extended:
            watermark_info_list: list[list[WatermarkInfo]] = []
            retention_policy_info_list: list[RetentionPolicyInfo] = []

            for topic in set(topic_info_list):
                watermark_info: list[WatermarkInfo] = self.get_watermark_info(
                    topic.topic_name)
                watermark_info_list.append(watermark_info)
                retention_policy = self.get_retention_policy_info(
                    topic.topic_name)
                retention_policy_info_list.append(retention_policy)

            df_watermark_info = entities_base.unpack_df_list(
                watermark_info_list)
            df_retention_policy = entities_base.dataclass_to_df(
                retention_policy_info_list)
            df = pd.merge(df, df_watermark_info,
                          on=["topic_name", "partition"],
                          how="inner")
            df = pd.merge(df,
                          df_retention_policy,
                          on=["topic_name"],
                          how="inner")

        return df

    def get_consumer_groups(self) -> pd.DataFrame:
        consumer_groups = self.admin_client.list_consumer_groups().result()
        if len(consumer_groups.errors) > 0:
            raise ValueError(
                f"Error while retrieving the consumer groups: {','.join(consumer_groups.errors)}"
            )
        consumer_group_list = [ConsumerGroup(
            group_id=group.group_id) for group in consumer_groups.valid]

        return entities_base.dataclass_to_df(consumer_group_list)

    def get_consumer_group_offsets(self, group_id: str, as_dataclass: bool = False) -> pd.DataFrame | list[ConsumerGroupsOffset]:
        consumer_group_offsets_request = [
            ConsumerGroupTopicPartitions(group_id=group_id)]
        offsets = self.admin_client.list_consumer_group_offsets(
            consumer_group_offsets_request, require_stable=True, request_timeout=10.0
        )
        consumer_group_offsets = []

        for group_id, future in offsets.items():
            result = future.result()

            for consumer_group_topic_partition in result.topic_partitions:
                consumer_group_offset = ConsumerGroupsOffset(
                    group_id=group_id,
                    topic_name=consumer_group_topic_partition.topic,
                    partition=consumer_group_topic_partition.partition,
                    offset=consumer_group_topic_partition.offset
                )
                consumer_group_offsets.append(consumer_group_offset)
        if as_dataclass:
            return consumer_group_offsets
        return entities_base.dataclass_to_df(consumer_group_offsets)

    def get_consumer_groups_offsets(self) -> pd.DataFrame:
        consumer_groups = self.admin_client.list_consumer_groups().result()

        if len(consumer_groups.errors) > 0:
            raise ValueError(
                f"Error while retrieving the consumer groups: {consumer_groups.errors}"
            )
        consumer_groups_with_offsets_dataclasses: list[pd.DataFrame] = []

        for group in consumer_groups.valid:
            offsets = self.get_consumer_group_offsets(
                group.group_id, as_dataclass=True)
            consumer_groups_with_offsets_dataclasses.append(offsets)

        return entities_base.unpack_df_list(consumer_groups_with_offsets_dataclasses)

    def get_offset_status(self,
                          consumer_context: Consumer,
                          topic: str | None = None) -> list[WatermarkInfo]:
        watermark_info_list: list[WatermarkInfo] = []

        committed = []
        committed_offset = COMMITED_OFFSET

        if isinstance(consumer_context, Consumer) and topic is not None:
            current_topic = topic
            consumer = consumer_context
        else:
            raise ValueError("Consumer context is not valid.")

        topics_dict: dict[str, TopicMetadata] = consumer.list_topics().topics
        partitions = topics_dict[current_topic].partitions
        topic_partition_list: list[TopicPartition] = [TopicPartition(
            topic=current_topic,
            partition=index)
            for index, _ in partitions.items()
        ]

        offset_list = consumer.position(topic_partition_list)
        try:
            committed = consumer.committed(topic_partition_list, timeout=2)
        except Exception:
            raise TimeoutError("Time out was reached")

        for offset in offset_list:
            watermark = consumer.get_watermark_offsets(
                topic_partition_list[offset.partition])

            if len(committed) > 0:
                committed_offset = committed[offset.partition].offset

            consumer_offset = offset.offset
            AUTO_OFFSET = Offset.EARLIEST.value
            if consumer_offset == COMMITED_OFFSET:
                consumer_offset = committed_offset
                if consumer_offset == COMMITED_OFFSET:
                    if AUTO_OFFSET == "earliest":
                        consumer_offset = watermark[0]
                    else:
                        consumer_offset = watermark[1]

            watermark_info = WatermarkInfo(
                topic_name=current_topic,
                partition=offset.partition,
                commited_offset=COMMITED_OFFSET,
                current_offset=offset.offset,
                calculated_offset=consumer_offset,
                low_watermark=watermark[0],
                high_watermark=watermark[1]
            )
            watermark_info_list.append(watermark_info)

        return watermark_info_list

    def plot_offset_status(self,
                           consumer: Consumer,
                           topic: str | None = None) -> None:
        if isinstance(consumer, Consumer) and topic is not None:
            offset = self.get_offset_status(consumer, topic=topic)
            current_topic = topic
        else:
            raise ValueError("Check the input data. A GenericConsumer or a "
                             "confluent_kafka.Consumer and a specific topic are mandatory")
        df = entities_base.dataclass_to_df(offset)
        df.plot(kind="bar", y=[
            "low_watermark",
            "calculated_offset",
            "high_watermark"],
            title=current_topic
        )
