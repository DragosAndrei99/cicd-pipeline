from aws_cdk import (
    aws_lambda as lambda_,
    aws_apigateway as apigw_,
    aws_ec2 as ec2,
    Duration,
)
from constructs import Construct

class API(Construct):
     def __init__(self, scope: Construct, construct_id: str,*, dynamodb_table_name: str, vpc, env: str) -> None:
        super().__init__(scope, construct_id)

        # Lambda function - GET
        self.scan_lambda_handler = lambda_.Function(
            self,
            f"ScanHandler{env}",
            function_name=f"scan_lambda_handler_{env}",
            runtime=lambda_.Runtime.PYTHON_3_9,
            environment={"DYNAMODB_TABLE_NAME": dynamodb_table_name},
            code=lambda_.Code.from_asset("backend/api/runtime"),
            handler="scan_lambda_handler.handler",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
            memory_size=1024,
            timeout=Duration.minutes(5),
        )

        # Lambda function - POST
        self.post_lambda_handler = lambda_.Function(
            self,
            f"PostHandler{env}",
            function_name=f"post_lambda_handler_{env}",
            runtime=lambda_.Runtime.PYTHON_3_9,
            environment={"DYNAMODB_TABLE_NAME": dynamodb_table_name},
            code=lambda_.Code.from_asset("backend/api/runtime"),
            handler="post_lambda_handler.handler",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
            memory_size=1024,
            timeout=Duration.minutes(5),
        )

        # Lambda function - PUT
        self.update_lambda_handler = lambda_.Function(
            self,
            f"PutHandler{env}",
            function_name=f"update_lambda_handler_{env}",
            runtime=lambda_.Runtime.PYTHON_3_9,
            environment={"DYNAMODB_TABLE_NAME": dynamodb_table_name},
            code=lambda_.Code.from_asset("backend/api/runtime"),
            handler="update_lambda_handler.handler",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
            memory_size=1024,
            timeout=Duration.minutes(5),
        )

        # Lambda function - DELETE
        self.delete_lambda_handler = lambda_.Function(
            self,
            f"DeleteHandler{env}",
            function_name=f"delete_lambda_handler_{env}",
            runtime=lambda_.Runtime.PYTHON_3_9,
            environment={"DYNAMODB_TABLE_NAME": dynamodb_table_name},
            code=lambda_.Code.from_asset("backend/api/runtime"),
            handler="delete_lambda_handler.handler",
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
            f"ApiGateway_{env}",
        )

        self.url = api_gw.url

        # Add /posts endpoint to API Gateway and enable CORS
        resource = api_gw.root.add_resource(
            'posts',
            default_cors_preflight_options=apigw_.CorsOptions(
                allow_methods=['GET', 'PUT', 'PATCH', 'POST','DELETE', 'OPTIONS'],
                allow_origins=apigw_.Cors.ALL_ORIGINS)
        )

        # Create lambda integration
        lambda_integration_get = apigw_.LambdaIntegration(
            self.scan_lambda_handler,
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

        lambda_integration_post = apigw_.LambdaIntegration(
            self.post_lambda_handler,
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

        lambda_integration_update = apigw_.LambdaIntegration(
            self.update_lambda_handler,
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

        lambda_integration_delete = apigw_.LambdaIntegration(
            self.delete_lambda_handler,
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
            'GET', lambda_integration_get,
            method_responses=[
                apigw_.MethodResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': True
                    }
                )
            ]
        )

        # Connect lambda to POST method
        resource.add_method(
            'POST', lambda_integration_post,
            method_responses=[
                apigw_.MethodResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': True
                    }
                )
            ]
        )

        # Connect lambda to PUT method
        resource.add_method(
            'PUT', lambda_integration_update,
            method_responses=[
                apigw_.MethodResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': True
                    }
                )
            ]
        )

        # Connect lambda to DELETE method
        resource.add_method(
            'DELETE', lambda_integration_delete,
            method_responses=[
                apigw_.MethodResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': True
                    }
                )
            ]
        )