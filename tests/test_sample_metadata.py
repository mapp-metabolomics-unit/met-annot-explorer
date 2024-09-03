import pandas as pd
import pytest

from met_annot_explorer.exceptions import (
    MissingRequiredColumnsError,
)
from met_annot_explorer.sample_metadata import SampleMetadata


@pytest.fixture
def sample_metadata():
    """Fixture to create a SampleMetadata instance with test data."""
    return SampleMetadata("tests/data/valid_sample_metadata.tsv")


@pytest.fixture
def invalid_sample_metadata_missing_columns():
    """Fixture to create a path to an invalid metadata file with missing required columns."""
    return "tests/data/invalid_sample_metadata_missing_columns.tsv"


def test_load_data(sample_metadata):
    """Test if data is loaded correctly."""
    assert sample_metadata.data is not None
    assert isinstance(sample_metadata.data, pd.DataFrame)


def test_get_column_names(sample_metadata):
    """Test if column names are retrieved correctly."""
    columns = sample_metadata.get_column_names()
    expected_columns = ["filename", "mapp_sample_id", "sample_type"]  # Add other expected columns
    assert set(expected_columns).issubset(set(columns))


def test_get_unique_values(sample_metadata):
    """Test if unique values in a column are retrieved correctly."""
    unique_values = sample_metadata.get_unique_values("solvant")
    expected_values = ["MeOH", "Heptane", "DCM"]  # Replace with actual unique values from your test data
    assert set(expected_values).issubset(set(unique_values))


def test_filter_by_value(sample_metadata):
    """Test if filtering by a column value works correctly."""
    filtered_data = sample_metadata.filter_by_value("solvant", "MeOH")
    assert not filtered_data.empty
    assert all(filtered_data["solvant"] == "MeOH")


def test_summary(sample_metadata):
    """Test if summary statistics are generated correctly."""
    summary = sample_metadata.summary()
    assert isinstance(summary, pd.DataFrame)
    assert "count" in summary.index


def test_missing_required_columns(invalid_sample_metadata_missing_columns):
    """Test if MissingRequiredColumnsError is raised when required columns are missing."""
    with pytest.raises(MissingRequiredColumnsError) as excinfo:
        SampleMetadata(invalid_sample_metadata_missing_columns)
    assert "Missing required columns" in str(excinfo.value)
