from dataclasses import asdict, dataclass

import pandas as pd


@dataclass(frozen=True)
class BaseEntity:
    def to_dict(self) -> dict:
        return asdict(self)


def dataclass_to_df(data: list[BaseEntity] | BaseEntity) -> pd.DataFrame:
    """Transforms a list of dataclasses (BaseEntity) into a pandas dataframe

    Args:
        data (list[BaseEntity] | BaseEntity): a single or list of BaseEntities

    Example:
        @dataclass
        class SomeClass(BaseEntity):
            a: str
            b: str

        some_instance = SomeClass(a="a", b="b")
        data = some_instance
        df = dataclass_to_df(some_instance)
           a  b
        0  a  b

    Returns:
        pd.DataFrame: dataframe
    """
    if not isinstance(data, list):
        data = [data]
    if any([element is None for element in data]):
        raise ValueError("Elements in list of dataclass are None")
    return pd.DataFrame([entity.to_dict() for entity in data])


def unpack_df_list(dataclass_list: list[list[BaseEntity]]) -> pd.DataFrame:
    df_list = [dataclass_to_df(element) for element in dataclass_list]
    return pd.concat(df_list, axis=0, ignore_index=True)
