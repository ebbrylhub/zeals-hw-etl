from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import os

def create_external_table_bikeshare():
    # Prepare Environment Variables
    project_id = os.environ['GOOGLE_CLOUD_PROJECT']
    dataset_id = os.environ['BQ_DATASET_NAME']
    bucket_name = os.environ['GCS_BUCKET_NAME']

    # Initialize BigQuery client
    client = bigquery.Client()

    # Table ID for the new external table
    table_id = f"{project_id}.{dataset_id}.bikeshare_table"

    # Source uri
    uri = f"gs://{bucket_name}/bikeshare/*"
    source_uri_prefix = (
        f"gs://{bucket_name}/bikeshare/"
    )

    # Define the schema of the table based on the public data
    schema = [
        bigquery.SchemaField("trip_id", "STRING"),
        bigquery.SchemaField("subscriber_type", "STRING"),
        bigquery.SchemaField("bike_id", "STRING"),
        bigquery.SchemaField("bike_type", "STRING"),
        bigquery.SchemaField("start_time", "TIMESTAMP"),
        bigquery.SchemaField("start_station_id", "INTEGER"),
        bigquery.SchemaField("start_station_name", "STRING"),
        bigquery.SchemaField("end_station_id", "STRING"),
        bigquery.SchemaField("end_station_name", "STRING"),
        bigquery.SchemaField("duration_minutes", "INTEGER"),
    ]

    # Set up the external configuration
    external_config = bigquery.ExternalConfig("PARQUET")
    external_config.source_uris = [uri]

    # Set up the table partitioning based on the start_time (daily partitioning)
    hive_partitioning_opts = bigquery.HivePartitioningOptions()
    hive_partitioning_opts.mode = "AUTO"
    hive_partitioning_opts.require_partition_filter = False
    hive_partitioning_opts.source_uri_prefix = source_uri_prefix

    external_config.hive_partitioning = hive_partitioning_opts

    # Create the table object
    table = bigquery.Table(table_id, schema=schema)
    table.external_data_configuration = external_config

    # Check if the table exists
    try:
        existing_table = client.get_table(table_id)  # Get the existing table

        # Update the existing table with the new external configuration
        existing_table.external_data_configuration = external_config
        updated_table = client.update_table(existing_table, ["external_data_configuration"])
        print(f"External table {table_id} updated successfully.")
    except NotFound:
        # Create the external table if it does not exist
        table = client.create_table(table, exists_ok=True)
        print(f"External table {table_id} created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    pass
