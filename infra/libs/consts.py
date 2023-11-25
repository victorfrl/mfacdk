from aws_cdk import Duration
from aws_cdk.aws_lambda import Runtime
from aws_cdk.aws_logs import RetentionDays

DEFAULT_RUNTIME = Runtime.PYTHON_3_11
COMPATIBLE_RUNTIME = [Runtime.PYTHON_3_11]
DEFAULT_LOG_RETENTION_IN_DAYS = RetentionDays.ONE_WEEK
DEFAULT_LAMBDA_HANDLER = "main.handler"
DEFAULT_LAMBDA_MEMORY = 512
DEFAULT_LAMBDA_RESERVED_CONCURRENCY = 5
DEFAULT_LAMBDA_TIMEOUT_IN_SECONDS = Duration.seconds(15)
