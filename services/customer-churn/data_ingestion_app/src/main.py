import os

import botocore
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import S3Options
from minio import Minio
from minio.error import S3Error
import logging
import glob
import boto3
from botocore.config import Config

# from apache_beam.io.aws.s3filesystem import S3FileSystem
# from apache_beam.io.filesystems import FileSystems
# FileSystems.register(S3FileSystem())
# os.environ["AWS_ACCESS_KEY_ID"] = ACCESS_KEY
# os.environ["AWS_SECRET_ACCESS_KEY"] = SECRET_KEY
# os.environ["AWS_REGION"] = "us-east-1"
# os.environ["AWS_S3_ENDPOINT"] = MINIO_ENDPOINT
# Setup Logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# MinIO Configuration
MINIO_ENDPOINT = os.getenv("AWS_S3_ENDPOINT", "localhost:9000")
ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "minioadmin")
SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "minioadmin")
RAW_BUCKET = "raw-data"
PROCESSED_BUCKET = "processed-data"

# MinIO Client Initialization
client = Minio(
    MINIO_ENDPOINT.replace("http://", "").replace("https://", ""),
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False
)
def create_bucket(bucket_name):
    """Create bucket if it doesn't exist."""
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        logging.info(f"Bucket '{bucket_name}' created.")
    else:
        logging.info(f"Bucket '{bucket_name}' already exists.")

def download_sample_data():
    """Download sample customer sales data."""
    # Corrected Dataset URL
    # url = "https://raw.githubusercontent.com/adesolabolu/Retail-Sales-Report/main/sales_data_sample.csv"
    
    local_file = "sales_data.csv"
    logging.info("Downloading sample sales data...")
    import pandas as pd
    df = pd.read_csv(local_file, encoding="ISO-8859-1")
    df.to_csv(local_file, index=False)
    logging.info(f"Data downloaded and saved as {local_file}.")
    return local_file

def preprocess_with_beam(input_file, output_file):
    """Process data using Apache Beam with SparkRunner."""
    # print("Starting preprocessing with Apache Beam (SparkRunner)...")

    #DOCKER CONFIG
    # pipeline_options = PipelineOptions([  
    # "--runner=PortableRunner",
    # "--job_endpoint=beam-job-server:8099",
    # "--artifact_endpoint=beam-job-server:8098",    
    # "--environment_type=DOCKER",
    # "--environment_config=apache/beam_python3.8_sdk:2.55.1"
    # ])
    # #PROCESS CONFIG
    #     # Define the JSON config in a variable
    # env_config = '{"command": "/opt/apache/beam/boot"}'
    # pipeline_options = PipelineOptions([
    #     "--runner=PortableRunner",
    #     "--job_endpoint=beam-job-server:8099",
    #     "--artifact_endpoint=beam-job-server:8098",
    #     "--environment_type=PROCESS",
    #     f"--environment_config={env_config}",
    #     "--no_validate"
    # ])
    #SIDECAR
    env_config = '{"command": "/opt/apache/beam/boot"}'
    pipeline_options = PipelineOptions([
        "--runner=PortableRunner",
        "--job_endpoint=beam-job-server:8099",
        "--artifact_endpoint=beam-job-server:8098",
        "--environment_type=EXTERNAL",
        "--environment_config=localhost:50000",
        "--requirements_file=./requirements.txt",
        "--no_validate"
    ])
    
      # Set S3 options
    s3_options = pipeline_options.view_as(S3Options)
    s3_options.s3_region_name = "us-east-1"
    s3_options.s3_access_key_id = ACCESS_KEY
    s3_options.s3_secret_access_key = SECRET_KEY
    s3_options.s3_endpoint_url = MINIO_ENDPOINT

    # Validation and Transformation Function
    def validate_and_transform(row):
        """Validation and preprocessing logic for retail sales data."""
        try:
           # print("Feature Engineering Started.....")
            # Split CSV row
            cols = row.split(",")

            # Ensure there are enough columns
            if len(cols) < 25:  # Expecting at least 25 columns based on dataset schema
                # logging.warning(f"Row has insufficient columns: {row}")
                return None

            # Parse required fields
            order_number = cols[0].strip()
            quantity_ordered = int(cols[1]) if cols[1].strip() else 1  # Default to 1 if missing
            price_each = float(cols[2]) if cols[2].strip() else 0.0  # Default to 0.0
            deal_size = cols[24].strip()  # Categorical field

            # Derived Features
            total_sales = quantity_ordered * price_each  # Calculate total sales
            is_large_deal = 1 if deal_size.lower() == 'large' else 0  # Binary flag for large deals
            # print("Feature Engineering Done.....")
            # Return processed row
            return f"{order_number},{quantity_ordered},{price_each},{total_sales},{is_large_deal}\n"

        except ValueError as e:  # Handle conversion errors
          #   print(f"Invalid data format in row: {row} - Error: {e}")
            return None
        except Exception as e:  # Catch unexpected errors
          #  print(f"Unexpected error processing row: {row} - Error: {e}")
            return None
    # print("Pipeline Configuring..")
    # Apache Beam Pipeline
    with beam.Pipeline(options=pipeline_options) as p:
        (
            p
            | "Read CSV" >> beam.io.ReadFromText("s3://raw-data/sales_data_01.csv", skip_header_lines=1)
            | "Filter Rows" >> beam.Filter(lambda row: len(row.split(",")) >= 25)  # Flexible filter
            | "Validate and Transform" >> beam.Map(validate_and_transform)
            | "Write Processed Data" >> beam.io.WriteToText("s3://processed-data/sales_data", file_name_suffix=".csv")
        )
        # Simple pipeline definition
    # with beam.Pipeline(options=pipeline_options) as p:
    #     (
    #         p
    #         | "Create Input" >> beam.Create(["Hello, World!", "Apache Beam", "Simple Pipeline"])
    #     )
    # print("Preprocessing complete.")

def upload_to_minio(file_path, bucket_name):
    """Upload data files to MinIO."""
    for file in glob.glob(file_path):  # Handle Apache Beam sharded outputs
        file_name = os.path.basename(file)
        client.fput_object(bucket_name, file_name, file)
        logging.info(f"Uploaded {file_name} to bucket '{bucket_name}'.")

def main():
    try:
        # Step 1: Create Buckets
        create_bucket(RAW_BUCKET)
        create_bucket(PROCESSED_BUCKET)

        # Step 2: Download Sample Data
      #  raw_file = download_sample_data()
        local_file = "sales_data_01.csv"
        upload_to_minio(local_file, RAW_BUCKET)

        # Step 3: Preprocess with Apache Beam and Spark
        processed_file = "processed_sales_data"
        preprocess_with_beam(local_file, processed_file)

        # Step 4: Upload Processed Data
        upload_to_minio(processed_file, PROCESSED_BUCKET)

    except S3Error as e:
        logging.error(f"MinIO Error: {e}")
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")

if __name__ == "__main__":
    main()
