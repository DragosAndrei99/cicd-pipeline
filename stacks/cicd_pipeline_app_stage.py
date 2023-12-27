import aws_cdk as cdk
from constructs import Construct
from stacks.cicd_pipeline_lambda_stack import ApiGWHttpApiLambdaDynamodbStack

# adding a new custom stage and defining the stack inside it
class ApiGWHttpApiLambdaDynamodbStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ApiGWHttpApiLambdaDynamodbStage = ApiGWHttpApiLambdaDynamodbStack(self, "ApiGWHttpApiLambdaDynamodbStack")
