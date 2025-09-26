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
    ['JOB_NAME', 'TERADATA_CONNECTION_NAME', 'TERADATA_TABLE'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

connection_name = args['TERADATA_CONNECTION_NAME']
table_name = args['TERADATA_TABLE']

try:
    logger.info(f"Attempting to connect to Teradata table: {table_name} using connection: {connection_name}")
    datasource = glueContext.create_dynamic_frame.from_options(
        connection_type="teradata",
        connection_options={
            "connectionName": connection_name,
            "dbtable": table_name,
            "numRows": 1  # Limit to 1 row for quick verification
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