import pandas as pd
import json


def parse_metadata(data_unit_file: str) -> dict:
    """Parses metadata from an OAS file

    Args:
        data_unit_file (str): path to the OAS sequence file

    Returns:
        dict: metadata of the file in dict
    """

    metadata = ",".join(pd.read_csv(data_unit_file, nrows=0).columns)
    metadata = json.loads(metadata)

    return metadata


def parse_sequence_data(data_unit_file: str) -> pd.DataFrame:
    """Parses actual sequence data from an OAS file

    Args:
        data_unit_file (str): path to the OAS sequence file

    Returns:
        pd.DataFrame: Df with sequence information corresponding to the datafile
    """

    sequence_df = pd.read_csv(data_unit_file, header=1)
    return sequence_df


def parse_file(data_unit_file: str) -> tuple[dict, pd.DataFrame]:
    """Parses a given OAS file and extracts both its metadata and sequence data

    Args:
        data_unit_file (str): path to the OAS sequence file

    Returns:
        tuple[dict, pd.DataFrame]: tuple of metadata and sequence data
    """

    metadata = parse_metadata(data_unit_file)
    sequence_data = parse_sequence_data(data_unit_file)

    return metadata, sequence_data


def 