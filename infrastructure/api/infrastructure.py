from aws_cdk import (
    aws_lambda as lambda_,
    aws_apigateway as apigw_,
    aws_ec2 as ec2,
    Duration,
    CfnOutput
)
from constructs import Construct

class API(Construct):
     def __init__(self, scope: Construct, construct_id: str,*, dynamodb_table_name: str, vpc) -> None:
        super().__init__(scope, construct_id)

        # Create the Lambda function
        self.api_handler = lambda_.Function(
            self,
            "ApiHandler",
            function_name="apigateway_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            environment={"DYNAMODB_TABLE_NAME": dynamodb_table_name},
            code=lambda_.Code.from_asset("app"),
            handler="index.handler",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
            memory_size=1024,
            timeout=Duration.minutes(5),
        )

        # Create API Gateway
        api_gw = apigw_.RestApi(
            self,
            "ApiGateway",
        )

        # Add resource to API Gateway and enable CORS
        resource = api_gw.root.add_resource(
            'example',
            default_cors_preflight_options=apigw_.CorsOptions(
                allow_methods=['GET', 'OPTIONS'],
                allow_origins=apigw_.Cors.ALL_ORIGINS)
        )

        # Create lambda integration
        lambda_integration = apigw_.LambdaIntegration(
            self.api_handler,
            proxy=False,
            integration_responses=[
                apigw_.IntegrationResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': "'*'"
                    }
                )
            ]
        )

        # Connect lambda to GET method
        resource.add_method(
            'GET', lambda_integration,
            method_responses=[
                apigw_.MethodResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': True
                    }
                )
            ]
        )

        CfnOutput(self, "apiUrl", value=api_gw.url)