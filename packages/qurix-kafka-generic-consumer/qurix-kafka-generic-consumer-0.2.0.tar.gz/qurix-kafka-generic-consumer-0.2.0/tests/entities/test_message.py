from datetime import datetime

import pytest

from qurix.kafka.entities.base import dataclass_to_df
from qurix.kafka.entities.message import Message


@pytest.fixture
def sample_messages() -> list[Message]:
    message_a = Message(
        partition=0,
        offset=1,
        timestamp=datetime.now(),
        length=100,
        key="some_key",
        header={"some_key": "a"},
        value="a"
    )
    return [message_a]


def test_messages(sample_messages: list[Message]):
    assert [len(sample_message.header) ==
            0 for sample_message in sample_messages]


def test_messages_dict(sample_messages: list[Message]):
    messages_dict_list = [sample_message.to_dict()
                          for sample_message in sample_messages]
    expected_column_names = [
        "partition",
        "offset",
        "timestamp",
        "length",
        "key",
        "header",
        "value",
    ]
    single_message = messages_dict_list[0]
    assert all([col in single_message for col in expected_column_names])


def test_message_df(sample_messages: list[Message]):
    df = dataclass_to_df(sample_messages)
    assert df["partition"].tolist() == [0]
    assert df["header"].tolist() == [{"some_key": "a"}]
