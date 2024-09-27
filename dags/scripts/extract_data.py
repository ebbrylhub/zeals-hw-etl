from google.cloud import bigquery
from google.cloud import storage
from google.oauth2 import service_account
from datetime import datetime, timedelta
import pandas as pd
import os

def extract_bigquery_data():
    # Path to your service account JSON file
    service_account_path = os.path.join(os.getcwd(), "dags/scripts/service_account.json")

    # Use service account credentials for both BigQuery and Storage clients
    credentials = service_account.Credentials.from_service_account_file(service_account_path)
    
    # Initialize BigQuery and Storage clients with the credentials
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    storage_client = storage.Client(credentials=credentials, project=credentials.project_id)

    # Get the previous day's date
    previous_day = (datetime(2024, 6, 30) - timedelta(1)).strftime('%Y-%m-%d')

    # Define the query to extract data for the previous day
    query = f"""
    SELECT * FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
    WHERE DATE(start_time) = '{previous_day}'
    """

    # Run the query and load results into a Pandas DataFrame
    df = client.query(query).to_dataframe()

    # Extract hour from the start_time column
    hour_iteration = pd.to_datetime(df['start_time']).dt.hour

    # Save the data into GCS in Parquet format, partitioned by date and hour
    bucket_name = 'bigquery-analytics-bucket'

    # Iterate over each hour to partition data by hour and upload to GCS
    for hour in set(hour_iteration):
        # Filter data for the specific hour
        hourly_data = df[pd.to_datetime(df['start_time']).dt.hour == hour]

        # Define the folder path using the start_time date and hour
        folder_path = f'bikeshare/date={previous_day}/hour={hour:02d}/data.parquet'
        
        # Save hourly DataFrame to Parquet format locally
        hourly_data.to_parquet("data.parquet")

        # Upload the file to GCS
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(folder_path)
        blob.upload_from_filename("data.parquet")

        print(f"Data for {previous_day} at hour {hour:02d} uploaded to {folder_path} in GCS.")

if __name__ == "__main__":
    extract_bigquery_data()