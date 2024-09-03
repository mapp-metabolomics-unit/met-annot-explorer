import pandas as pd
import pytest

from met_annot_explorer.annotation_table import AnnotationTable
from met_annot_explorer.exceptions import (
    DuplicateFeatureIDError,
    NonSerialFeatureIDError,
)


@pytest.fixture
def valid_annotation_table():
    """Fixture to create a valid AnnotationTable instance."""
    return AnnotationTable("tests/data/valid_annotation_table.tsv")


@pytest.fixture
def annotation_table_with_duplicate_feature_id():
    """Fixture to create a path to an annotation table with duplicate feature_id values."""
    return "tests/data/annotation_table_with_duplicate_feature_id.tsv"


@pytest.fixture
def annotation_table_with_non_serial_feature_id():
    """Fixture to create a path to an annotation table with non-serially incremented feature_id values."""
    return "tests/data/annotation_table_with_non_serial_feature_id.tsv"


def test_load_data(valid_annotation_table):
    """Test if data is loaded correctly."""
    assert valid_annotation_table.data is not None
    assert isinstance(valid_annotation_table.data, pd.DataFrame)


def test_get_column_names(valid_annotation_table):
    """Test if column names are retrieved correctly."""
    columns = valid_annotation_table.get_column_names()
    expected_columns = ["feature_id", "sources_IK2D", "canopus_molecularFormula"]  # Add other expected columns
    assert set(expected_columns).issubset(set(columns))


def test_get_unique_values(valid_annotation_table):
    """Test if unique values in a column are retrieved correctly."""
    unique_values = valid_annotation_table.get_unique_values("canopus_molecularFormula")
    expected_values = ["C7H13NO2", "C18H24O12"]  # Replace with actual unique values from your test data
    assert set(expected_values).issubset(set(unique_values))


def test_filter_by_value(valid_annotation_table):
    """Test if filtering by a column value works correctly."""
    filtered_data = valid_annotation_table.filter_by_value("canopus_molecularFormula", "C7H13NO2")
    assert not filtered_data.empty
    assert all(filtered_data["canopus_molecularFormula"] == "C7H13NO2")


def test_summary(valid_annotation_table):
    """Test if summary statistics are generated correctly."""
    summary = valid_annotation_table.summary()
    assert isinstance(summary, pd.DataFrame)
    assert "count" in summary.index


def test_validate_unique_feature_id(valid_annotation_table):
    """Test that feature_id is unique in a valid table."""
    valid_annotation_table._validate_unique_feature_id()  # Should not raise an error


def test_duplicate_feature_id(annotation_table_with_duplicate_feature_id):
    """Test that DuplicateFeatureIDError is raised for duplicate feature_id values."""
    with pytest.raises(DuplicateFeatureIDError) as excinfo:
        AnnotationTable(annotation_table_with_duplicate_feature_id)
    assert "Duplicate feature_id found:" in str(excinfo.value)


def test_validate_serially_incremented_feature_id(valid_annotation_table):
    """Test that feature_id is serially incremented in a valid table."""
    valid_annotation_table._validate_serially_incremented_feature_id()  # Should not raise an error


def test_non_serial_feature_id(annotation_table_with_non_serial_feature_id):
    """Test that NonSerialFeatureIDError is raised for non-serially incremented feature_id values."""
    with pytest.raises(NonSerialFeatureIDError) as excinfo:
        AnnotationTable(annotation_table_with_non_serial_feature_id)
    assert "Expected feature_id" in str(excinfo.value)
