from dataclasses import dataclass

import pandas as pd
import pytest

from qurix.kafka.entities.base import (BaseEntity, dataclass_to_df, unpack_df_list)


@dataclass(frozen=True)
class SampleData(BaseEntity):
    a: str
    b: list[int]


@pytest.fixture
def sample_data() -> SampleData:
    return SampleData("name", [1, 2, 3])


def test_base_entity(sample_data: SampleData):
    result = sample_data.to_dict()
    assert result["a"] == "name"
    assert result["b"] == [1, 2, 3]


def test_dataclass_to_df(sample_data: SampleData):
    result = dataclass_to_df(sample_data)
    assert isinstance(result, pd.DataFrame)
    assert result["a"].tolist() == ["name"]
    assert result["b"].tolist() == [[1, 2, 3]]


def test_unpack_df_list(sample_data: SampleData):
    sample_data_list = [sample_data, sample_data]
    result = unpack_df_list(sample_data_list)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert result["a"].tolist() == ["name", "name"]
    assert result["b"].tolist() == [[1, 2, 3], [1, 2, 3]]
