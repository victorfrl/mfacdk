from aws_cdk.aws_cloudfront import (
    AllowedMethods,
    BehaviorOptions,
    Distribution,
    ErrorResponse,
    OriginAccessIdentity,
    ViewerProtocolPolicy,
)
from aws_cdk.aws_cloudfront_origins import S3Origin
from aws_cdk.aws_s3 import BucketEncryption
from aws_cdk.aws_s3_deployment import BucketDeployment, Source
from constructs import Construct

from infra.libs.cloud import Bucket, CloudStack


class FrontStack(CloudStack):
    def __init__(
        self, scope: Construct, construct_id: str, backend_url: str, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.backend_url = backend_url

        self.bucket = Bucket(
            self,
            _id="StaticWebSiteBucket",
            encryption=BucketEncryption.S3_MANAGED,
            public_read_access=False,
        )

        BucketDeployment(
            scope=self,
            id="BucketDeployment",
            sources=[Source.asset("frontend/build")],
            destination_bucket=self.bucket,
        )

        origin_access = OriginAccessIdentity(self, "OriginAccessControl")
        s3_origin = S3Origin(self.bucket, origin_access_identity=origin_access)
        Distribution(
            self,
            "CloudFrontDistribution",
            default_behavior=BehaviorOptions(
                origin=s3_origin,
                viewer_protocol_policy=ViewerProtocolPolicy.ALLOW_ALL,
                allowed_methods=AllowedMethods.ALLOW_GET_HEAD_OPTIONS,
            ),
            error_responses=[
                ErrorResponse(
                    http_status=403,
                    response_page_path="/index.html",
                    response_http_status=200,
                )
            ],
        )
