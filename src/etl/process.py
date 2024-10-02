import pandas as pd
import json

def parse_metadata(data_unit_file: str) -> dict:
    """Parses metadata from an OAS file

    Args:
        data_unit_file (str): path to the OAS sequence file

    Returns:
        dict: metadata of the file in dict
    """
    metadata = ','.join(pd.read_csv(data_unit_file, nrows=0).columns)
    metadata = json.loads(metadata)

    return metadata