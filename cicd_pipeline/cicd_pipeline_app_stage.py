import aws_cdk as cdk
from constructs import Construct
from cicd_pipeline.cicd_pipeline_lambda_stack import MyLambdaStack

# adding a new custom stage and defining the lambda stack inside it


class LambdaAppStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambdaStack = MyLambdaStack(self, "LambdaStack")
