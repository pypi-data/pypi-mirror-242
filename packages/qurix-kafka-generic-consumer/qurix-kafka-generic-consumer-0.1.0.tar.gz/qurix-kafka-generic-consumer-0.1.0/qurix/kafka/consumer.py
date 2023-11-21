import datetime
import json
import logging
from typing import Any

import pandas as pd
from confluent_kafka import Consumer, KafkaError, TopicPartition

from qurix.kafka.entities.base import dataclass_to_df
from qurix.kafka.entities.config import ConsumerConfig, Offset
from qurix.kafka.entities.message import Message

logging.basicConfig(level=logging.INFO)


class GenericConsumer:
    """Kakfka consumer which fetches messages in a subscribed topic"""

    def __init__(self,
                 topic: str,
                 consumer_config: ConsumerConfig,
                 offset: Offset | None = None):
        self.consumer_client = Consumer(consumer_config.to_dict())
        self.topic = topic
        self.offset = offset.value if offset is not None else None

    def __enter__(self) -> "GenericConsumer":
        return self

    def __exit__(self, exec_type, exc_value, traceback) -> None:
        self.consumer_client.close()

    def set_offset(
        self,
        partition: int,
        offset_option: Offset = Offset.EXPLICIT,
        offset_value: int = 0,
        timestamp_dt: datetime = None,
    ) -> None:
        self.partition = partition
        watermark_offsets = self.consumer_client.get_watermark_offsets(
            TopicPartition(topic=self.topic, partition=partition))
        match offset_option:
            case Offset.EARLIEST:
                self.offset = watermark_offsets[0]
                logging.debug(
                    f"Last Offset for Partition {partition}: {self.offset}")
            case Offset.LATEST:
                self.offset = watermark_offsets[1]
                logging.debug(
                    f"Last Offset for Partition {partition}: {self.offset}")
            case Offset.LAST:
                self.offset = watermark_offsets[1] - 1
            case Offset.TIMESTAMP:
                unix_timestamp = int(timestamp_dt.timestamp()) * 1000
                tp = TopicPartition(self.topic, partition, unix_timestamp)
                offset_info = self.consumer_client.offsets_for_times([tp])
                offset = offset_info[0].offset if offset_info else None
                logging.debug(f"Timestamp: {timestamp_dt}, Offset: {offset}")
                self.offset = offset
            case _:
                self.offset = offset_value
        tp = TopicPartition(
            topic=self.topic, partition=partition, offset=self.offset)
        self.consumer_client.assign([tp])
        self.consumer_client.commit(offsets=[tp])

    def read_messages(
        self,
        num_messages: int = -1,
    ) -> pd.DataFrame:
        if self.offset is None:
            # Subscribe to the topic when offset is not set
            self.consumer_client.subscribe([self.topic])

        messages: list[Message] = []

        read = num_messages
        WAITING_TIME_SEC = 5
        while read:
            fetched_message = self.consumer_client.poll(WAITING_TIME_SEC)
            if fetched_message is None:
                logging.debug("No further data in topic")
                break
            if fetched_message.error():
                if fetched_message.error().code() == KafkaError._PARTITION_EOF:
                    logging.debug(
                        "Reached end of partition, waiting for new messages...")
                    break  # Exit the loop if no new messages to consume
                logging.debug(fetched_message.error())
            else:
                message = Message(
                    partition=fetched_message.partition(),
                    offset=fetched_message.offset(),
                    timestamp=datetime.datetime.fromtimestamp(
                        fetched_message.timestamp()[1] / 1000),
                    length=len(fetched_message.value()),
                    key=fetched_message.key(),
                    header=fetched_message.headers(),
                    value=fetched_message.value()
                )
                messages.append(message)
                read -= 1
                logging.debug(f"Remaining to read: {read}")
                if read == 0:  # Check if all desired messages are consumed
                    break
        df = dataclass_to_df(messages)
        self.consumer_client.close()
        return df

    def extend_df_with_header(self, df: pd.DataFrame) -> pd.DataFrame:
        HEADER_COL = "header"
        if HEADER_COL not in df:
            raise ValueError("Header column is not set")

        df_extended = df.copy()
        df_extended[HEADER_COL] = df_extended[HEADER_COL].apply(
            lambda x: dict(x))

        for index, row in df_extended.iterrows():
            header = row[HEADER_COL]
            for key, value in header.items():
                if isinstance(value, bytes):
                    value = value.decode("utf-8")
                new_column_name = "h_" + key
                df_extended.at[index,
                               new_column_name] = value if value is not None else None

        df_extended.drop(columns=[HEADER_COL], inplace=True)
        return df_extended

    @staticmethod
    def _process_json_data(json_data: dict | list | Any) -> pd.DataFrame:
        data = json.loads(json_data)
        if isinstance(data, list):
            return pd.DataFrame(data)
        elif isinstance(data, dict):
            return pd.json_normalize(data)
        else:
            raise ValueError("Invalid JSON structure")

    def extract_json_value(self, df: pd.DataFrame, value_column: str) -> pd.DataFrame:
        df_processed = df[value_column].apply(self._process_json_data)
        return pd.concat(df_processed.to_list(), ignore_index=True)
