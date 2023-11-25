import aws_cdk as cdk
from aws_cdk import aws_apigateway, aws_iam
from aws_cdk.aws_lambda import LayerVersion
from constructs import Construct

from infra.libs.cloud import CloudStack, DynamoDbTable, LambdaFunction, RestApi


class BackendStack(CloudStack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        _table = DynamoDbTable(
            self,
            "TasksTable",
            partition_key=cdk.aws_dynamodb.Attribute(
                name="task_id", type=cdk.aws_dynamodb.AttributeType.STRING
            ),
        )

        _layer_powertools = LayerVersion.from_layer_version_arn(
            self,
            "PowertoolsLayer",
            "arn:aws:lambda:us-east-1:017000801446:layer:AWSLambdaPowertoolsPythonV2-Arm64:47",
        )

        _function = LambdaFunction(
            self,
            "HandlerLambda",
            code=cdk.aws_lambda.Code.from_asset("src"),
            environment={"TABLE_NAME": _table.table_name},
            layers=[_layer_powertools],
        )

        _table.grant_read_write_data(_function)

        policy_document = aws_iam.PolicyDocument()
        self.api = RestApi(
            self,
            "ApiGateway",
            rest_api_name="MyApiGateway",
            default_cors_preflight_options=aws_apigateway.CorsOptions(
                allow_origins=cdk.aws_apigateway.Cors.ALL_ORIGINS,
                allow_methods=aws_apigateway.Cors.ALL_METHODS,
            ),
            policy=policy_document.add_statements(
                aws_iam.PolicyStatement(
                    effect=cdk.aws_iam.Effect.ALLOW,
                    actions=["execute-api:Invoke"],
                    resources=["execute-api:/*/*/*"],
                    principals=[aws_iam.ServicePrincipal("apigateway.amazonaws.com")],
                )
            ),
        )

        items = self.api.root.add_resource("items")
        items.add_method(
            "POST", aws_apigateway.LambdaIntegration(_function), authorization_type=None
        )
        items.add_method(
            "GET", aws_apigateway.LambdaIntegration(_function), authorization_type=None
        )
        get_items = items.add_resource("{id}")
        get_items.add_method(
            "GET", aws_apigateway.LambdaIntegration(_function), authorization_type=None
        )
