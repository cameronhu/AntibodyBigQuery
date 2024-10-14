from google.cloud import bigquery
import pandas as pd
from typing import Tuple


class BigQueryUploader:
    """
    Class responsible for uploading processed OAS data to Google BigQuery.

    Takes processed metadata, antibody, and sequence dataframes and uploads them
    to their respective tables in BigQuery, ensuring relationships between the tables
    are preserved.

    Attributes:
        project_id (str): GCP project ID where the BigQuery dataset is located
        dataset_id (str): BigQuery dataset ID where the tables reside
        client (bigquery.Client): BigQuery client instance for interaction
    """
