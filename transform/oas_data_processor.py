import pandas as pd
import json
import uuid
from transform.constants import COLUMN_ORDER


class OASDataProcessor:
    """
    Processing class for a single OAS file, adhering to the Antibody Database ERD.

    Takes a raw OAS file and splits the data into metadata, a linking antibody table, and a sequence table.
    Assigns a UID to every unpaired sequence, and retains the UID from the OAS paired sequences.
    If the file is a paired sequence, reformats the table to have the
    heavy and light chains vertically stacked (instead of horizontally concatenated).

    Attributes:
        data_unit_file (str): path to the OAS file to be processed
        metadata (json): metadata json associated with the file
        metadata_id (int): UID of the metadata
        is_paired (bool): paired or unpaired chain type of the file being processed
        columnar_order

    """

    def __init__(self, data_unit_file: str):
        """Initializes the OAS data processor with a given OAS sequence file.

        Args:
            data_unit_file (str): path to the OAS sequence file
        """
        self.data_unit_file = data_unit_file
        self.metadata = self.parse_metadata()
        self.metadata_id = self.metadata["metadata_id"]
        self.is_paired = self.metadata["Chain"] == "Paired"

    def generate_uid(self) -> str:
        """Unique Identifier generator function

        Returns:
            str: A newly generated UUID
        """
        return str(uuid.uuid4())

    def generate_uid_list(self, num_to_generate: int) -> list[str]:
        """Unique Identifier list generator function

        Args:
            num_to_generate (int): number of UUIDs to generate

        Returns:
            list[str]: list of UUIDs
        """
        return [self.generate_uid() for _ in range(num_to_generate)]

    def parse_metadata(self) -> dict:
        """Parses metadata from an OAS file and adds a unique identifier (UID)

        Args:
            data_unit_file (str): path to the OAS sequence file

        Returns:
            dict: metadata of the file in dict with a UID
        """
        metadata = ",".join(pd.read_csv(self.data_unit_file, nrows=0).columns)
        metadata = json.loads(metadata)

        # Add a UID to the metadata
        metadata["metadata_id"] = self.generate_uid()

        return metadata

    def generate_antibody_data(self, num_to_generate: int) -> pd.DataFrame:
        """Generates an Antibody Table for this study. Creates a UUID for each entity in the study,
        links every entity to its metadata (should be the same for every entry in the study),
        and provides additional data regarding if the data is paired.

        Args:
            num_to_generate (int): Number of antibody IDs to generate
            metadata (int): The metadata UID to assign to each entity
            is_paired (bool): If this dataset represents paired H/L chains

        Returns:
            pd.DataFrame: Antibody table with Antibody UID, linked Metadata UID, and Is_Paired boolean
        """
        antibody_uids = self.generate_uid_list(num_to_generate)
        antibody_data = pd.DataFrame(
            {
                "antibody_id": antibody_uids,
                "metadata_id": self.metadata_id,
                "is_paired": self.is_paired,
            }
        )
        return antibody_data

    def generate_individual_chain_df(
        self, sequence_df: pd.DataFrame, is_heavy: bool
    ) -> pd.DataFrame:
        """Splits a dataframe based off the given columns, then drops the suffixes
        Appends the Antibody UID and the Chain type to the final dataframe (in that order)

        Args:
            sequence_df (pd.DataFrame): Original full dataframe, with Antibody UID as the only non-mirrored column
            is_heavy (bool): if the chain to be parsed is heavy, or is light

        Returns:
            pd.DataFrame: Df with only the heavy or light chain data, with antibody_id and Chain columns appended
        """

        antibody_uid = sequence_df["antibody_id"]

        if is_heavy:
            suffix = "_heavy"
            chain = "Heavy"
        else:
            suffix = "_light"
            chain = "Light"

        columns = sequence_df.columns[sequence_df.columns.str.endswith(suffix)]

        df = sequence_df[columns].copy()
        df.columns = df.columns.str.replace(suffix, "")
        df["antibody_id"] = antibody_uid
        df["Chain"] = chain

        return df

    def process_paired_sequences(self, sequence_df: pd.DataFrame) -> pd.DataFrame:
        """Splits paired sequences into heavy and light chains; reconcatenates them vertically
        Retains pairing of heavy and light chains through linking to the same Antibody UID.
        Also retains heavy/light chain information that was encoded through column subscripts

        Args:
            sequence_df (pd.DataFrame): paired sequence df to split

        Returns:
            pd.DataFrame: New dataframe with heavy chains on top, corresponding light chains stacked below
        """
        # Splitting logic goes here

        # First, define the column indexes for the heavy and light chains
        # Split the heavy and light chain columns by their suffixes
        # Retain the remaining column (the antibody UID), and save it to be added to both split heavy and light dfs
        # For each heavy and light df, remove the subscripts and retain it as the ["Chain"] column
        # Add the Antibody UIDs to both heavy and light df: should be in the same order
        # Concatenate the heavy and light dfs vertically
        # Return a single df

        # Create the heavy chain df
        heavy_df = self.generate_individual_chain_df(sequence_df, is_heavy=True)

        # Create the light chain df
        light_df = self.generate_individual_chain_df(sequence_df, is_heavy=False)

        return_df = pd.concat([heavy_df, light_df])
        return_df.reset_index(drop=True, inplace=True)

        return return_df

    def parse_sequence_antibody_data(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Parses sequence data from an OAS file and adds a unique identifier for each sequence
        Creates an Antibody Table and links the sequences to an Antibody ID

        If metadata indicates paired chains, separates the H/L chains and assigns UIDs to each chain
        However, maintains paired information by linking both the H/L to one antibody entity (UID)

        Returns:
            pd.DataFrame: Sequence table with UID for each entity, already linked to antibody table
        """
        sequence_df = pd.read_csv(self.data_unit_file, header=1)
        num_seqs = len(sequence_df)

        # Generate an antibody table for this study, linking antibody sequences to metadata
        antibody_df = self.generate_antibody_data(num_seqs)
        sequence_df["antibody_id"] = antibody_df["antibody_id"]

        if self.is_paired:
            sequence_df = self.process_paired_sequences(sequence_df)
        else:
            sequence_df["Chain"] = self.metadata["Chain"]
            sequence_df["Isotype"] = self.metadata["Isotype"]
            sequence_df["sequence_id"] = self.generate_uid_list(num_seqs)

        sequence_df["Species"] = self.metadata["Species"]

        return sequence_df, antibody_df

    def process_file(self) -> tuple[dict, pd.DataFrame, pd.DataFrame]:
        """Parses a given OAS file and extracts both its metadata and sequence data
        Creates an antibody table linking sequences to their metadata
        Parses sequence data and links to antibodies differently if the data is paired chain data

        Returns:
            tuple[dict, pd.DataFrame, pd.DataFrame]: tuple of metadata (with UID) and sequence data (with UIDs)
        """
        sequence_df, antibody_df = self.parse_sequence_antibody_data()
        sequence_df = sequence_df.reindex(columns=COLUMN_ORDER)
        return self.metadata, antibody_df, sequence_df
