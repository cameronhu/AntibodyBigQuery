"""
Testing and timing script for first-pass implementation of process and load.
Every OASDataProcessor processes one file, and for every processed file there are 3 calls 
by BigQueryUploader to upload data to BigQuery

Benchmarking indicates large BigQuery client bottleneck for time
"""

import sys

sys.path.insert(0, "/home/cameronhu/oas_onboarding/utils")

import os
import time
from transform.oas_data_processor import OASDataProcessor
from load.big_query_uploader import BigQueryUploader
from load import constants
from timing_decorator import timing_decorator
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

    # Timing of processing portion
    timed_processor = timing_decorator(processor.process_file)
    (metadata, antibody_df, sequence_df), process_time = timed_processor()

    # Count the number of sequences
    num_sequences = sequence_df.shape[0]

    # Upload to BigQuery, timing
    timed_uploader = timing_decorator(uploader.upload_all)
    _, upload_time = timed_uploader(metadata, antibody_df, sequence_df)

    return process_time, upload_time, num_sequences


def process_and_upload_directory(file_list, dir_path):
    total_process_time = 0
    total_upload_time = 0
    total_sequences = 0

    for file in file_list:
        process_time, upload_time, num_sequences = process_and_upload(
            os.path.join(dir_path, file)
        )
        total_process_time += process_time
        total_upload_time += upload_time
        total_sequences += num_sequences

    return total_process_time, total_upload_time, total_sequences


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
    paired_process_time, paired_upload_time, num_paired_sequences = (
        process_and_upload_directory(paired_files, PAIRED_DIR)
    )

    # Process heavy unpaired files
    heavy_process_time, heavy_upload_time, num_heavy_sequences = (
        process_and_upload_directory(unpaired_heavy_files, UNPAIRED_HEAVY_DIR)
    )

    # Process light unpaired files
    light_process_time, light_upload_time, num_light_sequences = (
        process_and_upload_directory(unpaired_light_files, UNPAIRED_LIGHT_DIR)
    )

    total_time = (
        paired_process_time
        + heavy_process_time
        + light_process_time
        + paired_upload_time
        + heavy_upload_time
        + light_upload_time
    )

    print(
        f"Processing and uploading of {num_files} files per paired, heavy, and light chains completed in {total_time:.2f} seconds.\n",
        f"Paired chain processing of {num_paired_sequences} sequences took: {paired_process_time + paired_upload_time:.2f} seconds (process: {paired_process_time:.2f} seconds, upload: {paired_upload_time:.2f} seconds)\n",
        f"Heavy chain processing of {num_heavy_sequences} took: {heavy_process_time + heavy_upload_time:.2f} seconds (process: {heavy_process_time:.2f} seconds, upload: {heavy_upload_time:.2f} seconds)\n",
        f"Light chain processing of {num_light_sequences} took: {light_process_time + light_upload_time:.2f} seconds (process: {light_process_time:.2f} seconds, upload: {light_upload_time:.2f} seconds)\n",
    )
