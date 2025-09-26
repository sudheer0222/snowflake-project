import sys
import logging
import boto3
import json
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Get job parameters
args = getResolvedOptions(sys.argv,
    ['JOB_NAME', 'TERADATA_JDBC_URL', 'TERADATA_SECRET_NAME', 'TERADATA_TABLE'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

jdbc_url = args['TERADATA_JDBC_URL']
secret_name = args['TERADATA_SECRET_NAME']
table_name = args['TERADATA_TABLE']

# Retrieve credentials from AWS Secrets Manager
session = boto3.session.Session()
client = session.client(service_name='secretsmanager')
get_secret_value_response = client.get_secret_value(SecretId=secret_name)
secret = json.loads(get_secret_value_response['SecretString'])
user = secret['username']
password = secret['password']

try:
    logger.info(f"Attempting to connect to Teradata table: {table_name} using JDBC URL: {jdbc_url}")
    datasource = glueContext.create_dynamic_frame.from_options(
        connection_type="jdbc",
        connection_options={
            "url": jdbc_url,
            "user": user,
            "password": password,
            "dbtable": table_name
        }
    )
    df = datasource.toDF()
    if df.count() > 0:
        logger.info("Connection to Teradata database was successful.")
    else:
        logger.info("Connection established, but table is empty.")
except Exception as e:
    logger.error(f"Failed to connect to Teradata database: {e}")

job.commit()