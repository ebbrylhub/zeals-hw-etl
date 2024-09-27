from google.cloud import bigquery
from google.oauth2 import service_account
import os

def create_external_table(overwrite = False):
    # Path to your service account JSON file
    service_account_path = os.path.join(os.getcwd(), "dags/scripts/service_account.json")

    # Use service account credentials for BigQuery client
    credentials = service_account.Credentials.from_service_account_file(service_account_path)
    
    # Initialize BigQuery client
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    # Table ID for the new external table
    table_id = "temporal-sweep-436906-n8.analytics.bikeshare_table"

    # Source uri
    uri = "gs://bigquery-analytics-bucket/bikeshare/*"
    source_uri_prefix = (
        "gs://bigquery-analytics-bucket/bikeshare/"
    )

    # Set up the external configuration
    external_config = bigquery.ExternalConfig("PARQUET")
    external_config.source_uris = [uri]
    external_config.autodetect = True

    # Set up the table partitioning based on the start_time (daily partitioning)
    hive_partitioning_opts = bigquery.HivePartitioningOptions()
    hive_partitioning_opts.mode = "AUTO"
    hive_partitioning_opts.require_partition_filter = True
    hive_partitioning_opts.source_uri_prefix = source_uri_prefix

    external_config.hive_partitioning = hive_partitioning_opts

    # Create the table object
    table = bigquery.Table(table_id)
    table.external_data_configuration = external_config

    # Create the external table in BigQuery
    if overwrite:
        client.delete_table(table, not_found_ok=True)

    table = client.create_table(table, exists_ok=True)  # Make an API request

    print(f"External table {table_id} created successfully.")

if __name__ == "__main__":
    create_external_table(overwrite=True)
