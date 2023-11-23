from datetime import datetime

import pandas as pd
import pytest

from qurix.dataframe.anonymizer import (AnonymizeStrProvider, DataframeAnonymizer)


@pytest.fixture
def bigger_df() -> pd.DataFrame:
    df = pd.read_csv(
        "https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv")
    return df


@pytest.fixture
def example_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "float_col": [1.0, 2.0, 3.0, 4.0, 5.0],
            "int_col": [1, 2, 3, 4, 5],
            "str_col": ["a", "b", "c", "d", "e"],
            "date_col": [
                datetime(2021, 1, 1),
                datetime(2021, 1, 2),
                datetime(2021, 1, 3),
                datetime(2021, 1, 4),
                datetime(2021, 1, 5),
            ],
        }
    )


@pytest.fixture
def anonymize_str_map() -> dict:
    return {"str_col": AnonymizeStrProvider.GENDER}


@pytest.fixture
def anonymize_str_map_many() -> dict:
    return {"Sex": AnonymizeStrProvider.GENDER, "Name": AnonymizeStrProvider.PERSON_NAME}


@pytest.fixture
def white_list_col() -> list[str]:
    return ["float_col", "int_col"]


@pytest.fixture
def black_list_col() -> list[str]:
    return ["str_col", "date_col"]


@pytest.fixture
def anonymizer() -> DataframeAnonymizer:
    return DataframeAnonymizer()


def test_df_stats(
    anonymizer: DataframeAnonymizer, example_df: pd.DataFrame, anonymize_str_map: dict
):
    df_description: list[dict] = anonymizer.describe(
        example_df, anonymize_str_map)
    assert len(df_description) == 4
    expected_columns = [
        "col",
        "top",
        "min",
        "max",
        "freq",
        "unique",
        "count",
        "mean",
        "std",
        "dtype",
        "anonymize_str_provider",
    ]
    assert list(df_description[0].keys()) == expected_columns

    anonymized_str_col = [
        element for element in df_description if element["anonymize_str_provider"] is not None
    ]

    assert len(anonymized_str_col) == 1
    assert anonymized_str_col[0]["anonymize_str_provider"] == AnonymizeStrProvider.GENDER


def test_anonymize_dataframe(
    anonymizer: DataframeAnonymizer, example_df: pd.DataFrame, anonymize_str_map_many: dict
):
    anonymized_df = anonymizer.anonymize_dataframe(
        df=example_df, anonymize_str_map=anonymize_str_map_many
    )
    assert anonymized_df.shape == example_df.shape

    assert anonymized_df.dtypes.equals(example_df.dtypes)

    assert not anonymized_df.equals(example_df)

    assert list(anonymized_df.columns) == list(example_df.columns)

    assert anonymized_df.index.equals(example_df.index)


def test_anonymize_df_white_list(anonymizer: DataframeAnonymizer, example_df: pd.DataFrame, white_list_col: list[str], black_list_col: list[str]):
    anonymized_df = anonymizer.anonymize_dataframe(
        df=example_df, white_list=white_list_col)

    assert anonymized_df.shape == example_df.shape

    assert anonymized_df.dtypes.equals(example_df.dtypes)

    assert not anonymized_df.equals(example_df)

    assert list(anonymized_df.columns) == list(example_df.columns)

    assert anonymized_df.index.equals(example_df.index)


def test_anonymize_df_black_list(anonymizer: DataframeAnonymizer, example_df: pd.DataFrame, black_list_col: list[str]):
    anonymized_df = anonymizer.anonymize_dataframe(
        df=example_df, black_list=black_list_col)

    assert anonymized_df.shape == example_df.shape

    assert anonymized_df.dtypes.equals(example_df.dtypes)

    assert not anonymized_df.equals(example_df)

    assert list(anonymized_df.columns) == list(example_df.columns)

    assert anonymized_df.index.equals(example_df.index)


def test_anonymize_df_both_list(anonymizer: DataframeAnonymizer, example_df: pd.DataFrame, white_list_col: list[str]):
    anonymized_df = anonymizer.anonymize_dataframe(
        df=example_df, white_list=white_list_col)

    assert anonymized_df.shape == example_df.shape

    assert anonymized_df.dtypes.equals(example_df.dtypes)

    assert not anonymized_df.equals(example_df)

    assert list(anonymized_df.columns) == list(example_df.columns)

    assert anonymized_df.index.equals(example_df.index)


def test_big_df_anonymizer(
    anonymizer: DataframeAnonymizer, bigger_df: pd.DataFrame, anonymize_str_map_many: dict
):
    anonymized_df = anonymizer.anonymize_dataframe(
        bigger_df, anonymize_str_map_many)

    assert anonymized_df.shape == bigger_df.shape

    assert anonymized_df.dtypes.equals(bigger_df.dtypes)

    assert not anonymized_df.equals(bigger_df)

    assert list(anonymized_df.columns) == list(bigger_df.columns)

    assert anonymized_df.index.equals(bigger_df.index)
