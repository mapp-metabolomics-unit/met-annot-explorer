# met_annot_explorer/annotation_table.py

from typing import Any, List, Optional

import pandas as pd

from met_annot_explorer.exceptions import (
    DataLoadError,
    DataNotLoadedError,
    DuplicateFeatureIDError,
    FeatureIDNotFoundError,
    MissingColumnError,
    NonSerialFeatureIDError,
)


class AnnotationTable:
    def __init__(self, file_path: str):
        """
        Initialize the AnnotationTable class with a file path.

        Args:
            file_path (str): The path to the annotation table file.

        Raises:
            DataLoadError: If the data fails to load.
        """
        self.file_path = file_path
        self.data: Optional[pd.DataFrame] = None
        self._load_data()
        self._validate_unique_feature_id()
        self._validate_serially_incremented_feature_id()

    def _load_data(self) -> None:
        """Load the data from the file into a pandas DataFrame."""
        try:
            self.data = pd.read_csv(self.file_path, sep="\t")
        except Exception as e:
            raise DataLoadError(e) from e

    def _validate_unique_feature_id(self) -> None:
        """Validate that feature_id is unique."""
        if "feature_id" not in self.data.columns:
            raise FeatureIDNotFoundError()
        duplicated_ids = self.data[self.data["feature_id"].duplicated()]["feature_id"].tolist()
        if duplicated_ids:
            raise DuplicateFeatureIDError(duplicated_ids[0])

    def _validate_serially_incremented_feature_id(self) -> None:
        """Validate that feature_id is serially incremented starting from 1."""
        if "feature_id" not in self.data.columns:
            raise FeatureIDNotFoundError()
        feature_ids = self.data["feature_id"]
        expected_ids = list(range(1, len(feature_ids) + 1))
        for expected_id, actual_id in zip(expected_ids, feature_ids):
            if expected_id != actual_id:
                raise NonSerialFeatureIDError(expected_id, actual_id)

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
