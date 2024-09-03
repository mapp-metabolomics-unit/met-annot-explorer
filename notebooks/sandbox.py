from met_annot_explorer.annotation_table import AnnotationTable
from met_annot_explorer.sample_metadata import SampleMetadata

# Check the AnnotationTable class
# Initialize the class with the path to your table file
annotation_table = AnnotationTable("tests/data/mapp_batch_00083_met_annot_unified_horizontal.tsv")

# Get column names
columns = annotation_table.get_column_names()
print(columns)

# Get unique values from a specific column
unique_values = annotation_table.get_unique_values("canopus_molecularFormula")
print(unique_values)

# Filter the data by a specific value
filtered_data = annotation_table.filter_by_value("canopus_molecularFormula", "C7H13NO2")
print(filtered_data)

# Get a summary of the dataset
summary_stats = annotation_table.summary()
print(summary_stats)


# Check the SampleMetadata class
# Initialize the class with the path to your metadata file
sample_metadata = SampleMetadata("tests/data/mapp_batch_00083_metadata.tsv")

# Get column names
columns = sample_metadata.get_column_names()
print("Column Names:", columns)

# Get unique values from the 'solvant' column
unique_solvants = sample_metadata.get_unique_values("solvant")
print("Unique Solvants:", unique_solvants)


# Filter the data by 'solvant' column where the solvent is 'MeOH'
filtered_data = sample_metadata.filter_by_value("solvant", "MeOH")
print("Filtered Data:\n", filtered_data)


# Get a summary of the dataset
summary_stats = sample_metadata.summary()
print("Summary Statistics:\n", summary_stats)
