# met_annot_explorer/exceptions.py


class MetadataError(Exception):
    """Base class for exceptions in the metadata module."""

    pass


class FeatureIDNotFoundError(MetadataError):
    """Exception raised when the feature_id column is not found."""

    def __init__(self):
        super().__init__("feature_id column not found in the table.")


class DuplicateFeatureIDError(MetadataError):
    """Exception raised when duplicate feature_id values are found."""

    def __init__(self, feature_id):
        super().__init__(f"Duplicate feature_id found: {feature_id}")


class NonSerialFeatureIDError(MetadataError):
    """Exception raised when feature_id values are not serially incremented."""

    def __init__(self, expected_id, actual_id):
        super().__init__(f"Expected feature_id {expected_id}, but found {actual_id}")


class MissingColumnError(MetadataError):
    """Exception raised when a specified column is not found in the data."""

    def __init__(self, column_name):
        super().__init__(f"Column {column_name} not found in the table.")


class DataNotLoadedError(MetadataError):
    """Exception raised when an operation is attempted on data that hasn't been loaded."""

    def __init__(self):
        super().__init__("Data not loaded properly.")


class DataLoadError(MetadataError):
    """Exception raised when there is an error loading the data."""

    def __init__(self, original_exception):
        message = "Failed to load data"
        super().__init__(f"{message}: {original_exception!s}")


class MissingRequiredColumnsError(MetadataError):
    """Exception raised when required columns are missing."""

    def __init__(self, missing_columns):
        message = f"Missing required columns in the metadata file: {', '.join(missing_columns)}"
        super().__init__(message)


class IntensityColumnMismatchError(MetadataError):
    """Exception raised when intensity columns do not match SampleMetadata filenames."""

    def __init__(self, missing_columns):
        message = f"The following intensity columns do not correspond to any SampleMetadata filenames: {', '.join(missing_columns)}"
        super().__init__(message)
