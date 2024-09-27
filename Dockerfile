FROM apache/airflow:2.7.0

USER airflow

# Copy requirements.txt into the image
COPY requirements.txt /opt/airflow/requirements.txt

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

# Copy your DAGs
COPY dags/ /opt/airflow/dags/

# Set environment variables for Google Cloud credentials
ENV GOOGLE_APPLICATION_CREDENTIALS=/opt/airflow/dags/scripts/service_account.json
