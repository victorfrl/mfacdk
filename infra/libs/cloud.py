import typing

import constructs
from aws_cdk import aws_apigateway, aws_lambda, Duration, Tags, aws_logs, aws_dynamodb, Stack, aws_s3

from infra.libs import consts


# Create a wrapper of Stack
class CloudStack(Stack):
    def __init__(self, scope: constructs.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)


class RestApi(aws_apigateway.RestApi):
    def __init__(self, scope, _id, **kwargs):
        super().__init__(scope, _id, **kwargs)
        Tags.of(self).add("DEMO_CDK", _id)


class LambdaFunction(aws_lambda.Function):
    def __init__(
            self,
            scope: constructs.Construct,
            id: str,
            *,
            code: aws_lambda.Code,
            handler: str = consts.DEFAULT_LAMBDA_HANDLER,
            runtime: aws_lambda.Runtime = consts.DEFAULT_RUNTIME,
            environment: typing.Optional[typing.Mapping[str, str]] = None,
            layers: typing.Optional[typing.Sequence[aws_lambda.ILayerVersion]] = None,
            log_retention: typing.Optional[aws_logs.RetentionDays] = consts.DEFAULT_LOG_RETENTION_IN_DAYS,
            memory_size: typing.Optional[int] = consts.DEFAULT_LAMBDA_MEMORY,
            timeout: typing.Optional[Duration] = consts.DEFAULT_LAMBDA_TIMEOUT_IN_SECONDS,
    ):
        super().__init__(
            scope,
            id,
            code=code,
            handler=handler,
            runtime=runtime,
            architecture=aws_lambda.Architecture.ARM_64,
            environment=environment,
            layers=layers,
            log_retention=log_retention,
            memory_size=memory_size,
            timeout=timeout,
        )
        Tags.of(self).add("DEMO_CDK", id)


# Create a wrapper of aws_dynamodb
class DynamoDbTable(aws_dynamodb.Table):
    def __init__(self, scope: constructs.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)


class Bucket(aws_s3.Bucket):
    def __init__(self, scope: constructs.Construct, _id: str, **kwargs):
        super().__init__(scope, _id, **kwargs)
        Tags.of(self).add("DEMO_CDK", _id)
