# met_annot_explorer/feature_table.py

from typing import List, Optional

import pandas as pd

from met_annot_explorer.exceptions import (
    DataLoadError,
    DataNotLoadedError,
    IntensityColumnMismatchError,
    MissingColumnError,
)
from met_annot_explorer.sample_metadata import SampleMetadata


class FeatureTable:
    def __init__(self, file_path: str, sample_metadata: SampleMetadata):
        """
        Initialize the FeatureTable class with a file path and a SampleMetadata object.

        Args:
            file_path (str): The path to the feature table file.
            sample_metadata (SampleMetadata): An instance of the SampleMetadata class.

        Raises:
            DataLoadError: If the data fails to load.
            IntensityColumnMismatchError: If intensity columns do not match SampleMetadata filenames.
        """
        self.file_path = file_path
        self.sample_metadata = sample_metadata
        self.data: Optional[pd.DataFrame] = None
        self._load_data()
        self._rename_feature_id_column()
        self._validate_intensity_columns()

    def _load_data(self) -> None:
        """Load the data from the file into a pandas DataFrame."""
        try:
            self.data = pd.read_csv(self.file_path)
        except Exception as e:
            raise DataLoadError(e) from e

    def _rename_feature_id_column(self) -> None:
        """Rename the row ID column to feature_id if necessary."""
        if "row ID" in self.data.columns:
            self.data.rename(columns={"row ID": "feature_id"}, inplace=True)

    def _validate_intensity_columns(self) -> None:
        """Validate that all intensity columns correspond to filenames in the SampleMetadata."""
        intensity_columns = [col for col in self.data.columns if "Peak height" in col or "Peak area" in col]
        missing_columns = []

        # Extract valid filenames from the SampleMetadata
        valid_filenames = self.sample_metadata.data["filename"].tolist()

        for col in intensity_columns:
            # Check if the column prefix matches any valid filename
            prefix = col.split(" Peak")[0]  # Adjust split to retain filename before " Peak"
            if prefix not in valid_filenames:
                missing_columns.append(col)

        if missing_columns:
            raise IntensityColumnMismatchError(missing_columns)

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

    def get_unique_values(self, column_name: str) -> List[str]:
        """
        Get the unique values in a specified column.

        Args:
            column_name (str): The column name to explore.

        Returns:
            List[str]: The list of unique values in the column.
        """
        if self.data is not None:
            if column_name in self.data.columns:
                return self.data[column_name].unique().tolist()
            else:
                raise MissingColumnError(column_name)
        else:
            raise DataNotLoadedError()

    def filter_by_value(self, column_name: str, value: str) -> pd.DataFrame:
        """
        Filter the data by a specific value in a column.

        Args:
            column_name (str): The column name to filter on.
            value (str): The value to filter by.

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
