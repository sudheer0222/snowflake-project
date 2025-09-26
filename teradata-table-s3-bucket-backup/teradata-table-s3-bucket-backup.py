import sys
import logging
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Get job parameters
args = getResolvedOptions(sys.argv,
    ['JOB_NAME', 'TERADATA_CONNECTION_NAME', 'TERADATA_TABLE', 'S3_TARGET_PATH'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

connection_name = args['TERADATA_CONNECTION_NAME']
table_name = args['TERADATA_TABLE']
s3_path = args['S3_TARGET_PATH']

try:
    logger.info(f"Reading from Teradata table: {table_name} using connection: {connection_name}")
    datasource = glueContext.create_dynamic_frame.from_options(
        connection_type="teradata",
        connection_options={
            "connectionName": connection_name,
            "dbtable": table_name
        }
    )

    df = datasource.toDF()
    logger.info(f"Fetched {df.count()} rows from Teradata table: {table_name}")

    # (Optional) Transformations can be added here
    # Example: df = df.repartition(10)

    logger.info(f"Writing DataFrame to S3 path: {s3_path} in Parquet format")
    df.write.mode("overwrite").parquet(s3_path)
    logger.info("Write to S3 completed successfully.")

except Exception as e:
    logger.error(f"Error during Teradata to S3 backup: {e}")

job.commit()