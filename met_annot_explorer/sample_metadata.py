# met_annot_explorer/sample_metadata.py

from typing import Any, ClassVar, List, Optional

import pandas as pd

from met_annot_explorer.exceptions import (
    DataLoadError,
    DataNotLoadedError,
    MissingColumnError,
    MissingRequiredColumnsError,
)


class SampleMetadata:
    REQUIRED_COLUMNS: ClassVar[List[str]] = ["filename", "sample_id", "sample_type", "source_taxon"]

    def __init__(self, file_path: str):
        """
        Initialize the SampleMetadata class with a file path.

        Args:
            file_path (str): The path to the sample metadata file.

        Raises:
            DataLoadError: If the data fails to load.
            MissingRequiredColumnsError: If required columns are missing in the data.
        """
        self.file_path = file_path
        self.data: Optional[pd.DataFrame] = None
        self._load_data()
        self._validate_columns()

    def _load_data(self) -> None:
        """Load the data from the file into a pandas DataFrame."""
        try:
            self.data = pd.read_csv(self.file_path, sep="\t")
        except Exception as e:
            raise DataLoadError(e) from e

    def _validate_columns(self) -> None:
        """Validate that all required columns are present in the DataFrame."""
        missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in self.data.columns]
        if missing_columns:
            raise MissingRequiredColumnsError(missing_columns)

    def get_column_names(self) -> List[str]:
        """
        Get the list of column names in the table.

        Returns:
            List[str]: The list of column names.
        """
        if self.data is not None:
            return self.data.columns.tolist()
        else:
            raise DataNotLoadedError()

    def get_unique_values(self, column_name: str) -> List[Any]:
        """
        Get the unique values in a specified column.

        Args:
            column_name (str): The column name to explore.

        Returns:
            List[Any]: The list of unique values in the column.
        """
        if self.data is not None:
            if column_name in self.data.columns:
                return self.data[column_name].unique().tolist()
            else:
                raise MissingColumnError(column_name)
        else:
            raise DataNotLoadedError()

    def filter_by_value(self, column_name: str, value: Any) -> pd.DataFrame:
        """
        Filter the data by a specific value in a column.

        Args:
            column_name (str): The column name to filter on.
            value (Any): The value to filter by.

        Returns:
            pd.DataFrame: A DataFrame filtered by the specified column and value.
        """
        if self.data is not None:
            if column_name in self.data.columns:
                return self.data[self.data[column_name] == value]
            else:
                raise MissingColumnError(column_name)
        else:
            raise DataNotLoadedError()

    def summary(self) -> pd.DataFrame:
        """
        Provide a summary of the dataset, including the number of rows, columns, and basic statistics.

        Returns:
            pd.DataFrame: A DataFrame containing summary statistics.
        """
        if self.data is not None:
            return self.data.describe(include="all")
        else:
            raise DataNotLoadedError()
