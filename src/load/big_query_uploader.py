from google.cloud import bigquery
import pandas as pd
from typing import Tuple
from constants import *
import json


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

    def __init__(self, project_id: str, dataset_id: str):
        """Initializes the BigQueryUploader with the project and dataset information.

        Args:
            project_id (str): GCP project ID
            dataset_id (str): BigQuery dataset ID
        """
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.client = bigquery.Client(project=self.project_id)

    def upload_metadata(self, metadata: dict) -> None:
        """Uploads metadata to the Metadata table in BigQuery.

        Args:
            metadata (dict): Metadata dictionary with the structure {column_name: value}
        """
        table_id = f"{self.project_id}.{self.dataset_id}.metadata"
        metadata_df = pd.DataFrame([metadata])
        self._upload_dataframe(metadata_df, table_id)

    def upload_antibodies(self, antibody_df: pd.DataFrame) -> None:
        """Uploads antibody data to the Antibody table in BigQuery.

        Args:
            antibody_df (pd.DataFrame): DataFrame containing antibody data
        """
        table_id = f"{self.project_id}.{self.dataset_id}.antibody"
        self._upload_dataframe(antibody_df, table_id)

    def upload_sequences(self, sequence_df: pd.DataFrame) -> None:
        """Uploads sequence data to the Sequence table in BigQuery.

        Args:
            sequence_df (pd.DataFrame): DataFrame containing sequence data
        """
        table_id = f"{self.project_id}.{self.dataset_id}.sequence"
        self._upload_dataframe(sequence_df, table_id)

    def _upload_dataframe(self, df: pd.DataFrame, table_id: str) -> None:
        """Uploads a DataFrame to the specified BigQuery table.

        Args:
            df (pd.DataFrame): DataFrame to upload
            table_id (str): Full BigQuery table ID in the format 'project.dataset.table'
        """
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND
        )
        job = self.client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()  # Wait for the job to complete

    def upload_all(
        self, metadata: dict, antibody_df: pd.DataFrame, sequence_df: pd.DataFrame
    ) -> None:
        """Uploads all three data tables (metadata, antibody, sequence) to BigQuery in the correct order.

        Args:
            metadata (dict): Metadata dictionary
            antibody_df (pd.DataFrame): Antibody table DataFrame
            sequence_df (pd.DataFrame): Sequence table DataFrame
        """
        # 1. Upload metadata first (as Antibody and Sequence depend on it)
        self.upload_metadata(metadata)

        # 2. Upload antibody table (sequence table depends on it)
        self.upload_antibodies(antibody_df)

        # 3. Finally, upload the sequence table
        self.upload_sequences(sequence_df)


uploader = BigQueryUploader(project_id=GCP_PROJECT_ID, dataset_id=DATASET_ID)

with open("/home/cameronhu/oas_onboarding/data/metadata.json", "r") as f:
    data = f.read()
metadata = json.loads(data)


antibody_df = pd.read_csv(
    "/home/cameronhu/oas_onboarding/data/heavy_antibody_table.csv"
)
seq_df = pd.read_csv("/home/cameronhu/oas_onboarding/data/heavy_seq_table.csv")

uploader.upload_all(metadata, antibody_df, seq_df)
