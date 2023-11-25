import os

import aws_cdk as cdk

from infra.front_stack import FrontStack
from infra.simple_app_stack import BackendStack

app = cdk.App()

region = os.environ.get("CDK_DEPLOY_REGION", os.environ["CDK_DEFAULT_REGION"])
account = os.environ.get("CDK_DEPLOY_ACCOUNT", os.environ["CDK_DEFAULT_ACCOUNT"])
env = cdk.Environment(account=account, region=region)

backend_stack = BackendStack(scope=app, construct_id="BackendStack", env=env)
FrontStack(scope=app, construct_id="FrontedStack", backend_url=backend_stack.api.url, env=env)

app.synth()
