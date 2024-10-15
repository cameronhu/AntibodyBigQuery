from google.cloud import bigquery
from google.oauth2 import service_account
from constants import *


class BigQueryTableCreator:
    """
    Class responsible for creating the BigQuery tables for the OAS data.

    Attributes:
        project_id (str): GCP project ID
        dataset_id (str): BigQuery dataset ID where the tables will be created
        client (bigquery.Client): BigQuery client instance for interaction
    """

    def __init__(self, project_id: str, dataset_id: str, credentials=None):
        """
        Initializes the BigQueryTableCreator class.

        Args:
            project_id (str): The GCP project ID.
            dataset_id (str): The BigQuery dataset ID.
            credentials (google.auth.Credentials): Optional custom credentials for the BigQuery client.
        """
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.client = bigquery.Client(project=self.project_id, credentials=credentials)

    def create_metadata_table(self):
        """Creates the Metadata table in BigQuery."""
        table_id = f"{self.project_id}.{self.dataset_id}.metadata"

        schema = [
            bigquery.SchemaField("metadata_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("Species", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("Chain", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("Isotype", "STRING", mode="NULLABLE"),
            # Add additional metadata fields as needed
        ]

        table = bigquery.Table(table_id, schema=schema)
        self.client.create_table(table)
        print(f"Created table {table_id}")

    def create_antibody_table(self):
        """Creates the Antibody table in BigQuery."""
        table_id = f"{self.project_id}.{self.dataset_id}.antibody"

        schema = [
            bigquery.SchemaField("antibody_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("metadata_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("is_paired", "BOOLEAN", mode="REQUIRED"),
        ]

        table = bigquery.Table(table_id, schema=schema)
        self.client.create_table(table)
        print(f"Created table {table_id}")

    def create_sequence_table(self):
        """Creates the Sequence table in BigQuery."""
        table_id = f"{self.project_id}.{self.dataset_id}.sequence"

        schema = [
            bigquery.SchemaField("sequence_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("antibody_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("Chain", "STRING", mode="REQUIRED"),
            # Add additional sequence-specific fields (e.g., sequence data, annotations)
            bigquery.SchemaField("Species", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("Isotype", "STRING", mode="NULLABLE"),
            # Add any other fields that will be parsed from the sequence data
        ]

        table = bigquery.Table(table_id, schema=schema)
        self.client.create_table(table)
        print(f"Created table {table_id}")

    def create_all_tables(self):
        """Creates all tables: Metadata, Antibody, and Sequence."""
        self.create_metadata_table()
        self.create_antibody_table()
        self.create_sequence_table()


table_creator = BigQueryTableCreator(project_id=GCP_PROJECT_ID, dataset_id=DATASET_ID)
table_creator.create_all_tables()
# table_creator.create_metadata_table()
