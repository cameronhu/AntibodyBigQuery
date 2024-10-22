import sys
import os
import time
import argparse

sys.path.insert(0, "/home/cameronhu/oas_onboarding/utils")

from transform.oas_data_processor import OASDataProcessor
from load.big_query_uploader import BigQueryUploader
from load import constants
from timing_decorator import timing_decorator
from const_directories import *
from transform.batch import Batch  # Import the Batch class
from transform.data_manager import DataManager  # Import the DataManager class


# Function to process and upload a single batch of files using DataManager
def process_and_upload_batch(batch):
    # Instantiate DataManager with the files to process
    data_manager = DataManager(batch)

    # Timing of processing portion
    timed_process = timing_decorator(data_manager.process_files)
    _, process_time = timed_process()

    # Unpack processed data
    metadata_df, antibody_df, sequence_df = data_manager.get_batch_dataframes()

    # metadata.to_csv("metadata.csv")
    # antibody_df.to_csv("antibody_df.csv")
    # sequence_df.to_csv("sequence_df.csv")

    # Count the number of sequences
    num_sequences = sequence_df.shape[0]

    # Upload to BigQuery, timing
    timed_uploader = timing_decorator(uploader.upload_all)
    _, upload_time = timed_uploader(metadata_df, antibody_df, sequence_df)

    return process_time, upload_time, num_sequences


# Function to enumerate the batch_list and time each batch
def feed_batches(batch_list):
    total_process_time = 0
    total_upload_time = 0
    total_sequences = 0
    for i, batch in enumerate(batch_list):

        process_time, upload_time, num_sequences = process_and_upload_batch(batch)

        total_process_time += process_time
        total_upload_time += upload_time
        total_sequences += num_sequences

        print(
            f"For batch {i}, {num_sequences} processed, uploading took: {upload_time}, processing took: {process_time}"
        )

    return total_process_time, total_upload_time, total_sequences


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Parse arguments for OAS pipeline testing")
    parser.add_argument("num_batches", type=int)

    args = parser.parse_args()
    num_batches = args.num_batches

    # Initialize the uploader with your GCP project and dataset IDs
    uploader = BigQueryUploader(
        project_id=constants.GCP_PROJECT_ID, dataset_id=constants.DATASET_ID
    )

    # Uncomment when testing real batches

    # Create Batch instances for each directory with desired max batch size
    max_batch_size = 1 * 1024 * 1024 * 1024  # 1 GB
    paired_batch = Batch(PAIRED_DIR, max_batch_size)
    unpaired_heavy_batch = Batch(UNPAIRED_HEAVY_DIR, max_batch_size)
    unpaired_light_batch = Batch(UNPAIRED_LIGHT_DIR, max_batch_size)

    # Generate batches
    paired_batch.generate_batches()
    unpaired_heavy_batch.generate_batches()
    unpaired_light_batch.generate_batches()

    # Splice batch list to num_batches parsed
    paired_batch_list = paired_batch.get_batches()[:num_batches]
    unpaired_heavy_batch_list = unpaired_heavy_batch.get_batches()[:num_batches]
    unpaired_light_batch_list = unpaired_light_batch.get_batches()[:num_batches]

    # Make one manual batch for first test, just take the first 3 files from each directory

    # paired_files_local = sorted(os.listdir(PAIRED_DIR))
    # unpaired_heavy_files_local = sorted(os.listdir(UNPAIRED_HEAVY_DIR))
    # unpaired_light_files_local = sorted(os.listdir(UNPAIRED_LIGHT_DIR))

    # paired_files = []
    # unpaired_heavy_files = []
    # unpaired_light_files = []

    # for file in paired_files_local:
    #     paired_files.append(os.path.join(PAIRED_DIR, file))

    # for file in unpaired_heavy_files_local:
    #     unpaired_heavy_files.append(os.path.join(UNPAIRED_HEAVY_DIR, file))

    # for file in unpaired_light_files_local:
    #     unpaired_light_files.append(os.path.join(UNPAIRED_LIGHT_DIR, file))

    # paired_batch_list = [paired_files[:3]]
    # unpaired_heavy_batch_list = [unpaired_heavy_files[:3]]
    # unpaired_light_batch_list = [unpaired_light_files[:3]]

    # Process paired files in batches (limit by num_batches)
    paired_process_time, paired_upload_time, num_paired_sequences = feed_batches(
        paired_batch_list
    )

    # Process heavy unpaired files in batches (limit by num_batches)
    heavy_process_time, heavy_upload_time, num_heavy_sequences = feed_batches(
        unpaired_heavy_batch_list
    )

    # Process light unpaired files in batches (limit by num_batches)
    light_process_time, light_upload_time, num_light_sequences = feed_batches(
        unpaired_light_batch_list
    )

    total_time = (
        paired_process_time
        + heavy_process_time
        + light_process_time
        + paired_upload_time
        + heavy_upload_time
        + light_upload_time
    )

    total_sequences = num_heavy_sequences + num_light_sequences + num_paired_sequences

    sequences_per_second = total_sequences / total_time

    estimated_full_data_set_seconds = 2 * 10**9 / sequences_per_second
    estimated_full_data_set_hours = estimated_full_data_set_seconds / (60 * 60)
    estimated_full_data_set_days = estimated_full_data_set_hours / 24

    print(
        f"Processing and uploading of {num_batches} batches per paired, heavy, and light chains\n",
        f"Total processing of {total_sequences} completed in {total_time:.2f} seconds.\n\n"
        f"Paired chain processing of {num_paired_sequences} sequences took: {paired_process_time + paired_upload_time:.2f} seconds (process: {paired_process_time:.2f} seconds, upload: {paired_upload_time:.2f} seconds)\n",
        f"Heavy chain processing of {num_heavy_sequences} took: {heavy_process_time + heavy_upload_time:.2f} seconds (process: {heavy_process_time:.2f} seconds, upload: {heavy_upload_time:.2f} seconds)\n",
        f"Light chain processing of {num_light_sequences} took: {light_process_time + light_upload_time:.2f} seconds (process: {light_process_time:.2f} seconds, upload: {light_upload_time:.2f} seconds)\n\n",
        f"Sequence process and upload at rate of {sequences_per_second:.2f} sequences per second.\n",
        f"Predicted time for full 2 * 10^9 OAS sequences to be processed: {estimated_full_data_set_seconds:.2f} seconds, {estimated_full_data_set_hours:.2f} hours, {estimated_full_data_set_days:.2f} days",
    )
