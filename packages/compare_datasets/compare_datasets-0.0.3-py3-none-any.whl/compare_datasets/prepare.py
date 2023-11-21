from typing import List
import polars as pl
from collections import namedtuple
from tabulate import tabulate


class PrepareForComparison:
    """
    This class encapsulates the methods to compare two dataframes.

    Args:
        tested (polars.DataFrame): The dataframe to be tested.
        expected (polars.DataFrame): The expected dataframe.
        key (str): The column name to sort the dataframes.
        cast_numeric (bool, optional): Whether to cast numeric columns to a common type. Defaults to True.
        tolerance (int, optional): The numeric tolerance for comparison. Defaults to 6.

    Attributes:
        tested (polars.DataFrame): The dataframe to be tested.
        expected (polars.DataFrame): The expected dataframe.
        _tolerance (int): The numeric tolerance for comparison.
        _numeric_types (list): A list of numeric types for casting columns.
        _result (dict): A dictionary to store the comparison result.
        _mistmatched_schema (dict): A dictionary to store information about mismatched schemas.
        _row_and_column_counts (polars.DataFrame): A dataframe to store row counts.

    Methods:
        test_counts(): Compares the number of columns and rows between the dataframes.
        test_column_names(): Compares the column names between the dataframes.

    """

    @classmethod
    def __notPolars__(self, df):
        return not isinstance(df, pl.DataFrame)

    @classmethod
    def __convertToPolars__(self, df) -> namedtuple:
        return pl.DataFrame(df)

    def __init__(
        self,
        tested: pl.DataFrame,
        expected: pl.DataFrame,
        key = None,
        tolerance: float = 10e-6,
    ) -> None:
        self.getDataType = (
            lambda df, series: df[series].dtype
            if series in df.columns
            else "Does not exist"
        )
        self.tested = tested
        self.expected = expected
        self.key = key
        self.report = {}
        self._result = {}
        self._tolerance = tolerance
        self.row_and_column_counts = pl.DataFrame()
        self._numeric_types = [
            pl.Int64,
            pl.Float64,
            pl.UInt64,
            pl.Int32,
            pl.Float32,
            pl.UInt32,
            pl.Int16,
            pl.UInt16,
            pl.Int8,
            pl.Int8,
        ]
        self._datetime_types = ["Date", "Datetime", "Time"]
        self._boolean_types = ["Boolean"]
        self._string_types = [pl.Utf8]
        self._list_types = ["List"]
        self._category_types = [pl.Categorical]
        self.__intersection__ = set(self.expected.columns).intersection(
            set(self.tested.columns)
        )
        self.__union__ = set(self.expected.columns).union(set(self.tested.columns))
        if self.__notPolars__(self.tested):
            self.tested = self.__convertToPolars__(self.tested)
        if self.__notPolars__(self.expected):
            self.expected = self.__convertToPolars__(self.expected)
        self.__sort__()

        self.testColumnNames()
        self.testCounts()
        self.testSchema()
        self.__partitionOnColumnTypes__()
        self.matchRowCounts()

    def __sort__(self) -> None:
        if self.key is None:
            print("No key provided. Performing comparison without sorting.")
        else:
            self.tested = self.tested.sort(by=self.key, descending=False)
            self.expected = self.expected.sort(by=self.key, descending=False)

    def testCounts(self):
        """
        Compares the number of columns and rows between the dataframes.

        Returns:
            polars.DataFrame: A dataframe containing the counts and the difference between expected and tested dataframes.
        """
        row_and_column_counts = {
            "Attributes": ["No of columns", "No of rows"],
            "Expected": [len(self.expected.columns), self.expected.shape[0]],
            "Tested": [len(self.tested.columns), self.tested.shape[0]],
            "Difference": [
                len(self.expected.columns) - len(self.tested.columns),
                self.expected.shape[0] - self.tested.shape[0],
            ],
        }
        self.report[
            "count_report"
        ] = f"COUNT COMPARISON: \n{tabulate(row_and_column_counts, headers='keys', tablefmt='orgtbl')}"
        self._result["count_result"] = {
            "row_count_result": row_and_column_counts["Difference"][0] == 0,
            "column_count_result": row_and_column_counts["Difference"][1] == 0,
            "result": row_and_column_counts["Difference"][0] == 0
            and row_and_column_counts["Difference"][1] == 0,
        }

        return self.row_and_column_counts

    def testColumnNames(self):
        """
        Compares the column names between the dataframes.

        Returns:
            dict: A dictionary containing the intersection and difference between expected and tested dataframes.
        """

        self.column_comparison = {
            "Expected ∩ Tested": self.__intersection__,
            "Expected ∪ Tested": self.__union__,
            "Expected - Tested": set(self.expected.columns) - set(self.tested.columns),
            "Tested - Expected": set(self.tested.columns) - set(self.expected.columns),
        }
        self._result["column_names_result"] = (
            len(self.column_comparison["Expected ∩ Tested"])
            == len(self.expected.columns)
            == len(self.tested.columns)
        )

        self.report[
            "column_names_report"
        ] = f"COLUMNS COMPARISON: \n{tabulate(self.column_comparison, headers='keys', tablefmt='orgtbl')}"
        return self.column_comparison

    def matchRowCounts(self):
        if not self.key is None:
            common_rows = set(self.expected[self.key]).intersection(
                set(self.tested[self.key])
            )
            if self.expected.shape[0] != len(common_rows) or self.tested.shape[
                0
            ] != len(common_rows):
                print(
                    "The number of unique keys in the expected and tested dataframes do not match. \nTaking the intersection of the keys in both the dataframes to perform comparison."
                )
            self.expected = self.expected.filter(pl.col(self.key).is_in(common_rows))
            self.tested = self.tested.filter(pl.col(self.key).is_in(common_rows))
        else:
            if self.expected.shape[0] != self.tested.shape[0]:
                print(
                    "The number of rows in the expected and tested dataframes do not match. \nTruncating the dataframes to the same number of rows."
                )
                max_rows = max(self.expected.shape[0], self.tested.shape[0])
                self.expected = self.expected.head(max_rows)
                self.tested = self.tested.head(max_rows)
                print(
                    f"Dataframes have been truncated to the same number of rows. Since no key is provided, the first {max_rows} of both the dataframed have been taken."
                )

    def testSchema(self):
        all_columns = set(self.expected.columns).union(set(self.tested.columns))
        self.schema_comparison = {
            "Column": list(all_columns),
            "Expected": [
                self.getDataType(self.expected, column) for column in all_columns
            ],
            "Tested": [self.getDataType(self.tested, column) for column in all_columns],
        }
        self.mismatched_schema = [
            column
            for column in all_columns
            if self.getDataType(self.expected, column)
            != self.getDataType(self.tested, column)
        ]
        self._result["schema_result"] = len(self.mismatched_schema) == 0
        self.report[
            "schema_report"
        ] = f"SCHEMA COMPARISON: \n{tabulate(self.schema_comparison, headers=['Column', 'Expected', 'Tested'], tablefmt='orgtbl')}"
        return self._result["schema_result"]

    def __partitionOnColumnTypes__(self):
        intersection = self.__intersection__ - set(self.mismatched_schema)
        self.testSchema()
        self._numeric_columns = [
            column
            for column in intersection
            if self.getDataType(self.expected, column) in self._numeric_types
        ]
        self._datetime_columns = [
            column
            for column in intersection
            if self.getDataType(self.expected, column) in self._datetime_types
        ]
        self._boolean_columns = [
            column
            for column in intersection
            if self.getDataType(self.expected, column) in self._boolean_types
        ]
        self._string_columns = [
            column
            for column in intersection
            if self.getDataType(self.expected, column) in self._string_types
        ]
        self._list_columns = [
            column
            for column in intersection
            if self.getDataType(self.expected, column) in self._list_types
        ]
        self._category_columns = [
            column
            for column in intersection
            if self.getDataType(self.expected, column) in self._category_types
        ]

        self.column_list = {
            "Numeric Columns": self._numeric_columns,
            "Datetime Columns": self._datetime_columns,
            "Boolean Columns": self._boolean_columns,
            "String Columns": self._string_columns,
            "List Columns": self._list_columns,
        }
        self.report[
            "column_types_report"
        ] = f"COLUMN TYPES: \n{tabulate({k:v for k,v in self.column_list.items() if len(v) > 0}, headers='keys', tablefmt='orgtbl')}"

    def __str__(self):
        text = []
        text.append(self.report["count_report"])
        text.append(self.report["column_names_report"])
        text.append(self.report["schema_report"])
        text.append(self.report["column_types_report"])
        return "\n \n".join(text)
