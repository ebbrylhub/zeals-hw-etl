from datetime import datetime, timedelta
from google.cloud import bigquery
from google.cloud import storage
import logging
import os
import pandas as pd

def extract_bigquery_bikeshare(processing_date):
    # Prepare Environment Variables
    bucket_name = os.environ['GCS_BUCKET_NAME']
    
    # Initialize BigQuery and Storage clients with the credentials
    client = bigquery.Client()
    storage_client = storage.Client()

    # Define the query to extract data for the previous day
    query = f"""
    SELECT * FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
    WHERE DATE(start_time) = '{processing_date}'
    """

    # Run the query and load results into a Pandas DataFrame
    df = client.query(query).to_dataframe()

    # Extract hour from the start_time column
    hour_iteration = pd.to_datetime(df['start_time']).dt.hour

    # Save the data into GCS in Parquet format, partitioned by date and hour
    # Iterate over each hour to partition data by hour and upload to GCS
    for hour in set(hour_iteration):
        # Filter data for the specific hour
        hourly_data = df[pd.to_datetime(df['start_time']).dt.hour == hour]

        # Define the folder path using the start_time date and hour
        folder_path = f'bikeshare/date={processing_date}/hour={hour:02d}/data.parquet'
        
        # Save hourly DataFrame to Parquet format locally
        hourly_data.to_parquet(f"{processing_date}_{hour:02d}_data.parquet", compression=None, index=True)

        # Upload the file to GCS
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(folder_path)
        blob.upload_from_filename(f"{processing_date}_{hour:02d}_data.parquet")

        print(f"Data for {processing_date} at hour {hour:02d} uploaded to {folder_path} in GCS.")

if __name__ == "__main__":
    pass