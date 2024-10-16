import sys

sys.path.insert(0, "/home/cameronhu/oas_onboarding/utils")

import os
import time
from transform.oas_data_processor import OASDataProcessor
from load.big_query_uploader import BigQueryUploader
from load import constants
from time_decorator import timing_decorator
import argparse


# Constants for directories
PAIRED_DIR = "/export/share/cameronhu/oas/paired/paired_human"
UNPAIRED_HEAVY_DIR = (
    "/export/share/cameronhu/oas/unpaired/unpaired_human/unpaired_human_heavy"
)
UNPAIRED_LIGHT_DIR = (
    "/export/share/cameronhu/oas/unpaired/unpaired_human/unpaired_human_light"
)


# Function to process and upload a single file
def process_and_upload(file_path):
    processor = OASDataProcessor(file_path)
    metadata, antibody_df, sequence_df = processor.process_file()

    # Upload to BigQuery
    uploader.upload_all(metadata, antibody_df, sequence_df)


@timing_decorator
def process_and_upload_directory(file_list, dir_path):
    for file in file_list:
        process_and_upload(os.path.join(dir_path, file))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Parse arguments for OAS pipeline testing")
    parser.add_argument("num_files", type=int)

    args = parser.parse_args()

    num_files = args.num_files

    # Initialize the uploader with your GCP project and dataset IDs
    uploader = BigQueryUploader(
        project_id=constants.GCP_PROJECT_ID, dataset_id=constants.DATASET_ID
    )

    # Get the first num_files paired and unpaired files
    paired_files = sorted(os.listdir(PAIRED_DIR))[:num_files]
    unpaired_heavy_files = sorted(os.listdir(UNPAIRED_HEAVY_DIR))[:num_files]
    unpaired_light_files = sorted(os.listdir(UNPAIRED_LIGHT_DIR))[:num_files]

    # Uncomment when ready to test

    # Process paired files
    process_and_upload_directory(paired_files, PAIRED_DIR)

    # Process heavy unpaired files
    process_and_upload_directory(unpaired_heavy_files, UNPAIRED_HEAVY_DIR)

    # Process light unpaired files
    process_and_upload_directory(unpaired_light_files, UNPAIRED_LIGHT_DIR)

    # print(
    #     f"Processing and uploading of {num_files} files completed in {total_time:.2f} seconds. \n",
    #     f"Paired processing took: {paired_time} seconds \n",
    #     f"Heavy processing took: {heavy_time} seconds \n",
    #     f"Light processing took: {light_time} seconds \n",
    # )
