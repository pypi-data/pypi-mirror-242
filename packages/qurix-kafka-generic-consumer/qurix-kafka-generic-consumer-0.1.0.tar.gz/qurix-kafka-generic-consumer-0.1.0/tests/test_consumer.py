import json
import pandas as pd
import pytest

from qurix.kafka.entities.config import Offset
from qurix.kafka.consumer import GenericConsumer
from tests.common import TEST_TOPIC_NAME, consumer_config, teardown, tearup


@pytest.fixture
def tear_up_kafka():
    tearup(5)
    yield
    teardown(5)


@pytest.fixture
def kakfa_consumer_mock(tear_up_kafka) -> GenericConsumer:
    return GenericConsumer(topic=TEST_TOPIC_NAME, consumer_config=consumer_config)


@pytest.fixture
def sample_header() -> pd.DataFrame:
    data = {
        'header': [
            [('source', b'Testdriver'), ('target', b'Confluent_kafka')],
            [('source', b'AnotherSource'), ('target', b'AnotherTarget')],
        ]
    }
    return pd.DataFrame(data)


@pytest.mark.integration_test
def test_consumer_read_messages(kakfa_consumer_mock: GenericConsumer):
    messages = kakfa_consumer_mock.read_messages()
    assert isinstance(messages, pd.DataFrame)
    assert len(messages["value"]) > 0
    assert json.loads(messages['value'][0].decode(
        "utf-8")) == {"some": "message"}


@pytest.mark.integration_test
def test_consumer_with_partition_offset(kakfa_consumer_mock: GenericConsumer):
    kakfa_consumer_mock.set_offset(partition=0,
                                   offset_value=1000,
                                   offset_option=Offset.EXPLICIT)
    messages = kakfa_consumer_mock.read_messages()
    assert len(messages["value"]) > 0


@pytest.mark.integration_test
def test_extend_df_with_header(kakfa_consumer_mock: GenericConsumer,
                               sample_header: pd.DataFrame):
    extended_df = kakfa_consumer_mock.extend_df_with_header(sample_header)
    assert 'header' not in extended_df.columns
    assert 'h_source' in extended_df.columns
    assert 'h_target' in extended_df.columns
    assert extended_df['h_source'].tolist() == ['Testdriver', 'AnotherSource']
    assert extended_df['h_target'].tolist(
    ) == ['Confluent_kafka', 'AnotherTarget']


@pytest.mark.integration_test
def test_extract_json_value(kakfa_consumer_mock: GenericConsumer,
                            sample_header: pd.DataFrame):

    sample_header['JsonColumn'] = [
        '{"key": "value"}',
        '{"key": "value2"}'
    ]
    concatenated_df = pd.concat(
        [sample_header, sample_header], ignore_index=True)
    result_df = kakfa_consumer_mock.extract_json_value(
        df=concatenated_df, value_column='JsonColumn')
    assert result_df.shape == (4, 1)
    assert result_df['key'].tolist() == ['value', 'value2', 'value', 'value2']
