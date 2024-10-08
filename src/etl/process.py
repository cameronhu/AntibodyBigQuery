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


def generate_antibody_data(
    num_to_generate: int, metadata_uid: int, is_paired: bool
) -> pd.DataFrame:
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

    antibody_data = pd.DataFrame()

    # Generate UIDs
    antibody_uids = generate_uid_list(num_to_generate)

    # Attribute UIDs to a column
    antibody_data["antibody_uid"] = antibody_uids

    # Assign the same metadata uid to each antibody entity
    antibody_data["metadata_uid"] = metadata_uid

    # Assign Is_Paired boolean if Metadata[Chain] = Paired
    antibody_data["is_paired"] = is_paired

    return antibody_data


def split_paired_sequences(sequence_df: pd.DataFrame) -> pd.DataFrame:
    """Splits paired sequences into heavy and light chains; reconcatenates them vertically
    Retains pairing of heavy and light chains through linking to the same Antibody UID

    Args:
        sequence_df (pd.DataFrame): paired sequence df to split

    Returns:
        pd.DataFrame: New dataframe with heavy chains on top, corresponding light chains stacked below
    """
    # Should be 198 columns: 99 for each chain, + 1 for Antibody UID
    # assert sequence_df.shape[1] == 199

    return sequence_df


def parse_sequence_antibody_data(
    data_unit_file: str, metadata: dict
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Parses sequence data from an OAS file and adds a unique identifier for each sequence
    Creates an Antibody Table and links the sequences to an Antibody ID

    If metadata indicates paired chains, separates the H/L chains and assigns UIDs to each chain
    However, maintains paired information by linking both the H/L to one antibody entity (UID)

    Args:
        data_unit_file (str): path to the OAS sequence file

    Returns:
        pd.DataFrame: Sequence table with UID for each entity, already linked to antibody table
    """

    # Determine if the dataset is paired or unpaired
    is_paired = metadata["Chain"] == "Paired"
    metadata_uid = metadata["metadata_uid"]

    # Read the sequence data starting from the second row
    sequence_df = pd.read_csv(data_unit_file, header=1)

    # Number of unpaired or paired sequences in the original dataset
    num_seqs = len(sequence_df)

    # Generate an antibody table for this study, linking antibody sequences to metadata. Link to the sequences
    antibody_df = generate_antibody_data(len(sequence_df), metadata_uid, is_paired)
    sequence_df["antibody_uid"] = antibody_df["antibody_uid"]

    if is_paired:
        sequence_df = split_paired_sequences(sequence_df)

    else:
        sequence_df["Isotype"] = metadata["Isotype"]

        # Add a UID column for each sequence row, only for unpaired (paired already contains UIDs)
        sequence_df["sequence_id"] = generate_uid_list(num_seqs)

    return sequence_df, antibody_df


def parse_file(data_unit_file: str) -> tuple[dict, pd.DataFrame, pd.DataFrame]:
    """Parses a given OAS file and extracts both its metadata and sequence data
    Creates an antibody table linking sequences to their metadata
    Parses sequence data and links to antibodies differently if the data is paired chain data

    Args:
        data_unit_file (str): path to the OAS sequence file

    Returns:
        tuple[dict, pd.DataFrame, pd.DataFrame]: tuple of metadata (with UID) and sequence data (with UIDs)
    """

    # Extract metadata and add a UID
    metadata = parse_metadata(data_unit_file)

    # Extract sequence data and generate UID
    sequence_df, antibody_df = parse_sequence_antibody_data(data_unit_file, metadata)

    return metadata, antibody_df, sequence_df
