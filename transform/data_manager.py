import pandas as pd
from transform.oas_data_processor import OASDataProcessor


class DataManager:
    """
    Class that handles the processing of a batch of OAS files.
    Manages multiple OASDataProcessors to process the files and concatenate their inputs into a final batch dataframe.
    Parallelizes the processing (and potentially concatenation) done by the OASDataProcessors

    Attributes:
        file_paths (list): the batch data - list of OAS file paths to be processed
        batch_metadata_df (Dataframe): concatenated metadata df for all files in batch
        batch_antibody_df (Dataframe): concatenated antibody df for all files in batch
        batch_sequence_df (Dataframe): concatenated sequence df for all files in batch

    """

    def __init__(self, file_paths):
        """
        Initialize the manager with a list of file paths.
        """
        self.file_paths = file_paths
        self.batch_metadata_df = pd.DataFrame()
        self.batch_antibody_df = pd.DataFrame()
        self.batch_sequence_df = pd.DataFrame()

    def process_files(self):
        """
        Processes all the OAS files and concatenates the results into batch DataFrames.
        """
        for file_path in self.file_paths:
            # Instantiate OASDataProcessor for each file
            processor = OASDataProcessor(file_path)
            metadata_df, antibody_df, sequence_df = processor.process_file()

            # Concatenate the results into the batch DataFrames
            self.batch_metadata_df = pd.concat(
                [self.batch_metadata_df, metadata_df], ignore_index=True
            )

            self.batch_antibody_df = pd.concat(
                [self.batch_antibody_df, antibody_df], ignore_index=True
            )
            self.batch_sequence_df = pd.concat(
                [self.batch_sequence_df, sequence_df], ignore_index=True
            )

    def get_batch_dataframes(self):
        """
        Returns the batch DataFrames after processing.
        """
        return self.batch_metadata_df, self.batch_antibody_df, self.batch_sequence_df
