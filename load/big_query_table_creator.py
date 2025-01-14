from google.cloud import bigquery
import load.constants as constants


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

        schema = constants.METADATA_SCHEMA

        table = bigquery.Table(table_id, schema=schema)
        self.client.create_table(table)
        print(f"Created table {table_id}")

    def create_antibody_table(self):
        """Creates the Antibody table in BigQuery."""
        table_id = f"{self.project_id}.{self.dataset_id}.antibody"

        schema = constants.ANTIBODY_SCHEMA

        table = bigquery.Table(table_id, schema=schema)
        table.clustering_fields = ["is_paired"]
        self.client.create_table(table)
        print(f"Created table {table_id}")

    def create_sequence_table(self):
        """Creates the Sequence table in BigQuery."""
        table_id = f"{self.project_id}.{self.dataset_id}.sequence"

        schema = constants.SEQUENCE_SCHEMA

        table = bigquery.Table(table_id, schema=schema)

        # Create clustering based off species, chain, isotype
        table.clustering_fields = ["Chain", "Species", "Isotype"]

        self.client.create_table(table)
        print(f"Created table {table_id}")

    def create_all_tables(self):
        """Creates all tables: Metadata, Antibody, and Sequence."""
        self.create_metadata_table()
        self.create_antibody_table()
        self.create_sequence_table()


if __name__ == "__main__":
    table_creator = BigQueryTableCreator(
        project_id=constants.GCP_PROJECT_ID, dataset_id=constants.DATASET_ID
    )
    table_creator.create_all_tables()
