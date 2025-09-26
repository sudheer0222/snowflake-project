import sys
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql import DataFrame

## Glue job parameters
args = getResolvedOptions(sys.argv,
                          ['JOB_NAME',
                           'TERADATA_CONNECTION_NAME',
                           'TERADATA_TABLE',
                           'S3_TARGET_PATH'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Parameters
connection_name = args['TERADATA_CONNECTION_NAME']
table_name = args['TERADATA_TABLE']
s3_path = args['S3_TARGET_PATH']

# Create Glue DynamicFrame from Teradata
datasource = glueContext.create_dynamic_frame.from_options(
    connection_type="teradata",
    connection_options={
        "connectionName": connection_name,
        "dbtable": table_name
    }
)

# Convert to DataFrame if you want to apply transformations
df: DataFrame = datasource.toDF()

# (Optional) Add partitioning or transformations here
# df = df.repartition(10)  # Example: repartition for parallelism

# Write to S3 in Parquet format
(
    df.write
    .mode("overwrite")   # or "append"
    .parquet(s3_path)
)

job.commit()