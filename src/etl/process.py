import pandas as pd
import json
import uuid


def generate_uid() -> str:
    """Unique Identifier generator function

    Returns:
        str:
    """
    return str(uuid.uuid4())


def generate_uid_list(num_to_generate: int) -> list[str]:
    """Unique Identifier list generator function

    Args:
        num_to_generate (int): number of UUIDs to generate

    Returns:
        list[str]: list of UUIDs
    """
    return [generate_uid() for _ in range(num_to_generate)]


def parse_metadata(data_unit_file: str) -> dict:
    """Parses metadata from an OAS file and adds a unique identifier (UID)

    Args:
        data_unit_file (str): path to the OAS sequence file

    Returns:
        dict: metadata of the file in dict with a UID
    """

    metadata = ",".join(pd.read_csv(data_unit_file, nrows=0).columns)
    metadata = json.loads(metadata)

    # Add a UID to the metadata
    metadata["metadata_uid"] = generate_uid()

    return metadata


def generate_antibody_data(num_to_generate: int, metadata: dict) -> pd.DataFrame:
    """Generates an Antibody Table for this study. Creates a UUID for each entity in the study,
    links every entity to its metadata (should be the same for every entry in the study),
    and provides additional data regarding if the data is paired

    Args:
        num_to_generate (int): Number of antibody IDs to generate
        metadata (dict): The metadata dict, which contains a UID as an attribute, to assign with each entity

    Returns:
        pd.DataFrame: Antibody table with Antibody UID, linked Metadata UID, and Is_Paired boolean
    """

    antibody_data = pd.DataFrame()

    # Generate UIDs
    antibody_uids = generate_uid_list(num_to_generate)

    # Attribute UIDs to a column
    antibody_data["antibody_uid"] = antibody_uids

    # Assign the same metadata uid to each antibody entity
    antibody_data["metadata_uid"] = metadata["metadata_uid"]

    # Assign Is_Paired boolean if Metadata[Chain] = Paired
    antibody_data["is_paired"] = metadata["Chain"] == "Paired"

    return antibody_data


def parse_sequence_data(data_unit_file: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Parses actual sequence data from an OAS file and adds a unique identifier for each row
    Also generates an Antibody Table which links sequence data to metadata

    Args:
        data_unit_file (str): path to the OAS sequence file

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: The first DataFrame is the Sequence Table,
        the second DataFrame is the Antibody Table linking sequences to metadata
    """

    # Read the sequence data starting from the second row
    sequence_df = pd.read_csv(data_unit_file, header=1)

    # Number of sequences in this df
    num_seqs = len(sequence_df)

    # Add a UID column for each sequence row
    sequence_df["sequence_uid"] = generate_uid_list(num_seqs)

    return sequence_df


def link_sequence_antibody_data(
    sequence_data: pd.DataFrame, antibody_data: pd.DataFrame
) -> None:
    """Given a Sequence df and Antibody df, link each sequence to an Antibody UID

    Args:
        sequence_data (pd.DataFrame): Df of sequences, with annotation data from OAS
        antibody_data (pd.DataFrame): Df of antibodies, with metadata UIDs to link
    """

    # Link sequences to antibodies and metadata
    sequence_data["antibody_uid"] = antibody_data["antibody_uid"]

    return


def parse_file(data_unit_file: str) -> tuple[dict, pd.DataFrame, pd.DataFrame]:
    """Parses a given OAS file and extracts both its metadata and sequence data

    Args:
        data_unit_file (str): path to the OAS sequence file

    Returns:
        tuple[dict, pd.DataFrame]: tuple of metadata (with UID) and sequence data (with UIDs)
    """

    # Extract metadata and add a UID
    metadata = parse_metadata(data_unit_file)

    # Extract sequence data and generate UID
    sequence_data = parse_sequence_data(data_unit_file, metadata["file_uid"])

    # Generate an antibody table for this study, linking antibody sequences to metadata
    antibody_data = generate_antibody_data()

    return metadata, antibody_data, sequence_data
