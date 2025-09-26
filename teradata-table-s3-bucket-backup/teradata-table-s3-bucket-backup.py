import sys
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext

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

# Read from Teradata using Glue connection
datasource = glueContext.create_dynamic_frame.from_options(
    connection_type="teradata",
    connection_options={
        "connectionName": connection_name,
        "dbtable": table_name
    }
)

# Convert to Spark DataFrame
df = datasource.toDF()

# (Optional) Transformations can be added here
# Example: df = df.repartition(10)

# Write DataFrame to S3 in Parquet format
df.write.mode("overwrite").parquet(s3_path)

job.commit()