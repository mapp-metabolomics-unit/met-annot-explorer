import pandas as pd
import pytest

from met_annot_explorer.exceptions import (
    IntensityColumnMismatchError,
)
from met_annot_explorer.feature_table import FeatureTable
from met_annot_explorer.sample_metadata import SampleMetadata


@pytest.fixture
def sample_metadata():
    """Fixture to create a SampleMetadata instance with valid test data."""
    return SampleMetadata("tests/data/valid_sample_metadata.tsv")


@pytest.fixture
def valid_feature_table(sample_metadata):
    """Fixture to create a FeatureTable instance with valid test data."""
    return FeatureTable("tests/data/valid_feature_table.csv", sample_metadata)


@pytest.fixture
def invalid_feature_table(sample_metadata):
    """Fixture to create a path to an invalid feature table with inconsistent intensity columns."""
    return "tests/data/invalid_feature_table.csv"


def test_load_data(valid_feature_table):
    """Test if data is loaded correctly."""
    assert valid_feature_table.data is not None
    assert isinstance(valid_feature_table.data, pd.DataFrame)


def test_get_column_names(valid_feature_table):
    """Test if column names are retrieved correctly."""
    columns = valid_feature_table.get_column_names()
    assert len(columns) > 0


def test_get_unique_values(valid_feature_table):
    """Test if unique values in a column are retrieved correctly."""
    unique_values = valid_feature_table.get_unique_values("feature_id")
    assert isinstance(unique_values, list)


def test_filter_by_value(valid_feature_table):
    """Test if filtering by a column value works correctly."""
    filtered_data = valid_feature_table.filter_by_value("feature_id", 12)
    assert not filtered_data.empty
    assert all(filtered_data["feature_id"] == 12)


def test_summary(valid_feature_table):
    """Test if summary statistics are generated correctly."""
    summary = valid_feature_table.summary()
    assert isinstance(summary, pd.DataFrame)
    assert "count" in summary.index


def test_inconsistent_intensity_columns(invalid_feature_table, sample_metadata):
    """Test if IntensityColumnMismatchError is raised when intensity columns do not match SampleMetadata filenames."""
    with pytest.raises(IntensityColumnMismatchError) as excinfo:
        FeatureTable(invalid_feature_table, sample_metadata)
    assert "do not correspond to any SampleMetadata filenames" in str(excinfo.value)
