import random
from datetime import date, timedelta
from enum import Enum
from typing import Any

import numpy as np
import pandas as pd
from mimesis import Address, Generic, Person
from mimesis.locales import Locale


class AnonymizeStrProvider(str, Enum):
    ADDRESS = "address"
    GENDER = "gender"
    PERSON_NAME = "person"
    OTHER = "other"


class DataframeAnonymizer:
    COL_KEY = "col"
    MEAN_KEY = "mean"
    MIN_KEY = "min"
    MAX_KEY = "max"
    STD_KEY = "std"
    COUNT_KEY = "count"
    FREQ_KEY = "freq"
    UNIQUE_KEY = "unique"
    TOP_KEY = "top"
    ANONYMIZE_STR_PROVIDER = "anonymize_str_provider"
    DTYPE_KEY = "dtype"

    def describe(
        self, df: pd.DataFrame, anonymize_str_map: dict[str, AnonymizeStrProvider] = {}
    ) -> list[dict]:
        """Returns a list of dictionary descriptive statistics for each column of a dataframe.

        df is generic. replace_value contains the index col of the original
        df and the "label" of the value, e.g. {2: "gender"}

        Based on these statistics, the anonymizer will generate synthetic columns.

        Args:
            df (pd.DataFrame): original df
            anonymize_str_map (dict[str, AnonymizeStrProvider]): mapping with the name of the str column
            and the prefered anonymize string provider, e.g. "gender" (AnonymizeStrProvider.GENDER)

        Returns:
            list[dict]: list of dictionaries with statistics like min, max, freq, etc. for each col
        """
        df_description_dict: dict[str, Any] = df.describe(include="all").to_dict()

        df_col_description_list = [
            {
                self.COL_KEY: col,
                self.TOP_KEY: df_description_dict[col].get(self.TOP_KEY),
                self.MIN_KEY: df_description_dict[col].get(self.MIN_KEY),
                self.MAX_KEY: df_description_dict[col].get(self.MAX_KEY),
                self.FREQ_KEY: df_description_dict[col].get(self.FREQ_KEY),
                self.UNIQUE_KEY: df_description_dict[col].get(self.UNIQUE_KEY),
                self.COUNT_KEY: df_description_dict[col].get(self.COUNT_KEY),
                self.MEAN_KEY: df_description_dict[col].get(self.MEAN_KEY),
                self.STD_KEY: df_description_dict[col].get(self.STD_KEY),
                self.DTYPE_KEY: df[col].dtype,
                self.ANONYMIZE_STR_PROVIDER: anonymize_str_map.get(col),
            }
            for col in df.columns
        ]

        return df_col_description_list

    @staticmethod
    def _replace_with_positive_min_value(list_values: list, min_value: float | int) -> list:
        return np.array([item if item >= 0 else min_value for item in list_values])

    def _anonymize_float(
        self,
        mean_value: float,
        std_value: float,
        count_value: int,
        min_value: float,
        max_value: float,
    ) -> list[float]:
        """Generates a random sequence of int based on descriptive statistics
        with a defined length.

        It checks if the list should contain negative values. These are replaced
        by the minimum value

        Args:
            mean_value (float): mean value
            std_value (float): standard deviation
            count_value (float): frequency
            min_value (float): minimum
            max_value (float): maximum

        Returns:
            list[float]: "anonymized" list of float values
        """
        input_negative: bool = min_value < 0
        random_generator = np.random.default_rng(1234)
        normal_draw = random_generator.normal(mean_value, std_value, int(count_value))
        sorted_result = np.sort(normal_draw)
        sorted_result[0] = min_value
        sorted_result[-1] = max_value
        random_generator.shuffle(sorted_result)
        anonymized_floats = sorted_result.astype(float)
        if not input_negative:
            anonymized_floats = self._replace_with_positive_min_value(anonymized_floats, min_value)
        return anonymized_floats.astype(float)

    def _anonymize_int(
        self,
        mean_value: float,
        std_value: float,
        count_value: float,
        min_value: float,
        max_value: float,
    ) -> list[int]:
        """Generates a random sequence of int based on descriptive statistics
        with a defined length.

        It checks if the list should contain negative values. These are replaced
        by the minimum value

        Args:
            mean_value (float): mean value
            std_value (float): standard deviation
            count_value (float): frequency
            min_value (float): minimum
            max_value (float): maximum

        Returns:
            list[int]: "anonymized" list of int
        """
        input_negative: bool = min_value < 0
        random_generator = np.random.default_rng(1234)
        floats = random_generator.normal(mean_value, std_value, int(count_value))
        ints = np.round(floats).astype(int)
        sorted_ints = np.sort(ints)
        sorted_ints[0] = min_value
        sorted_ints[-1] = max_value
        random_generator.shuffle(sorted_ints)
        anonymized_ints = sorted_ints.astype(int)
        if not input_negative:
            anonymized_ints = self._replace_with_positive_min_value(anonymized_ints, min_value)
        return anonymized_ints.astype(int)

    @staticmethod
    def _anonymize_str(
        count_value: int, unique_value: str, anonymize_str_provider: AnonymizeStrProvider
    ) -> list[str]:
        """Generates a random sequence of str with a defined length

        Args:
            count_value (int): length of original column
            unique_value (str): unique generated values
            anonymize_str_provider (AnonymizeStrProvider): enum with available anonymize string providers

        Returns:
            list[str]: anononymized string list
        """
        generic = Generic(locale=Locale.DE)
        person = Person(locale=Locale.DE)
        address = Address(locale=Locale.DE)
        providers = {
            None: lambda nb: [generic.text.word() for _ in range(nb)],
            AnonymizeStrProvider.GENDER: lambda nb: [person.gender() for _ in range(nb)],
            AnonymizeStrProvider.ADDRESS: lambda nb: [address.address() for _ in range(nb)],
            AnonymizeStrProvider.PERSON_NAME: lambda nb: [person.full_name() for _ in range(nb)],
        }
        string_list = providers[anonymize_str_provider](unique_value)
        random_strings = []
        counter = 0
        while len(random_strings) < count_value:
            random_strings.append(string_list[counter])
            counter = (counter + 1) % len(string_list)
        random.shuffle(random_strings)
        return random_strings

    @staticmethod
    def _anonymize_date(start_date: date, end_date: date, count: int) -> list:
        date_list = [
            start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
            for _ in range(count)
        ]
        return date_list

    def anonymize_column(self, col_dict: dict) -> dict | None:
        col_dtype = col_dict[self.DTYPE_KEY]
        col_count = col_dict[self.COUNT_KEY]
        col_mean = col_dict[self.MEAN_KEY]
        col_min = col_dict[self.MIN_KEY]
        col_max = col_dict[self.MAX_KEY]
        col_std = col_dict[self.STD_KEY]
        col_unique = col_dict[self.UNIQUE_KEY]
        match col_dtype:
            case "float64":
                return self._anonymize_float(col_mean, col_std, col_count, col_min, col_max)
            case "int64":
                return self._anonymize_int(col_mean, col_std, col_count, col_min, col_max)
            case "object":
                col_value = col_dict[self.ANONYMIZE_STR_PROVIDER]
                return self._anonymize_str(col_count, col_unique, col_value)
            case "datetime64[ns]":
                return self._anonymize_date(col_min, col_max, col_count)
            case _:
                return None

    def anonymize_dataframe(
        self, df: pd.DataFrame,
        white_list: list[str] | None = None,
        black_list: list[str] | None = None,
        anonymize_str_map: dict[str, AnonymizeStrProvider] = {},
    ) -> pd.DataFrame:
        """Method to anonymize all dataframe columns

        Args:
            df (pd.DataFrame): dataframe to anonymize
            value (dict): value to replace a certain column

        Returns:
            pd.DataFrame: anonymized dataframe
    """
        if white_list is not None and black_list is not None:
            common_columns = [col_name for col_name in white_list if col_name in black_list]
            if common_columns:
                raise ValueError(f"Columns {common_columns} present in both whitelist and blacklist.Please check the list")

        anonymized_df = df.copy()
        df_description = self.describe(df, anonymize_str_map)
        for col_dict in df_description:
            col_name = col_dict[self.COL_KEY]

            if (white_list is None or col_name in white_list) and (black_list is None or col_name not in black_list):
                col_anonymized = self.anonymize_column(col_dict)
                if col_anonymized is not None:
                    anonymized_df[col_name] = col_anonymized

        return anonymized_df
