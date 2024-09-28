FROM apache/airflow:2.7.0

# Root User for Installing Google Cloud SDK
USER root

# Install Google Cloud SDK
RUN apt-get update -y && \
    apt-get install -y apt-transport-https ca-certificates gnupg && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
    | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
    apt-get update -y && \
    apt-get install google-cloud-cli -y

# Airflow User for Installing Dependencies and Authentication
USER airflow

# Copy requirements.txt into the image
COPY requirements.txt /opt/airflow/requirements.txt

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

# Copy your DAGs
COPY dags/ /opt/airflow/dags/

# Set environment variables for Google Cloud credentials
ENV GOOGLE_CLOUD_PROJECT=temporal-sweep-436906-n8
ENV GCS_BUCKET_NAME=bigquery-analytics-bucket
ENV BQ_DATASET_NAME=analytics

# Authenticate using a service account key
RUN gcloud auth activate-service-account --key-file=/opt/airflow/dags/scripts/service_account.json && \
    gcloud config set project $GOOGLE_CLOUD_PROJECT
