import os
import time
from transform.oas_data_processor import OASDataProcessor
from load.big_query_uploader import BigQueryUploader
from load import constants

# Constants for directories
PAIRED_DIR = "/export/share/cameronhu/oas/paired"
UNPAIRED_DIR = "/export/share/cameronhu/oas/unpaired"

# Initialize the uploader with your GCP project and dataset IDs
uploader = BigQueryUploader(
    project_id=constants.GCP_PROJECT_ID, dataset_id=constants.DATASET_ID
)

# Get the first 10 paired and unpaired files
paired_files = sorted(os.listdir(PAIRED_DIR))[:10]
unpaired_files = sorted(os.listdir(UNPAIRED_DIR))[:10]


# Function to process and upload a single file
def process_and_upload(file_path):
    processor = OASDataProcessor(file_path)
    metadata, antibody_df, sequence_df = processor.process_file()

    # Upload to BigQuery
    uploader.upload_all(metadata, antibody_df, sequence_df)


# Uncomment when ready to test

# # Time the whole process
# start_time = time.time()

# # Process paired files
# for file in paired_files:
#     process_and_upload(os.path.join(PAIRED_DIR, file))

# # Process unpaired files
# for file in unpaired_files:
#     process_and_upload(os.path.join(UNPAIRED_DIR, file))

# # Calculate the time taken
# end_time = time.time()
# total_time = end_time - start_time

# print(f"Processing and uploading completed in {total_time:.2f} seconds.")
