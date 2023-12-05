import aws_cdk as cdk
from constructs import Construct
from aws_cdk.aws_lambda import Function, InlineCode, Runtime

# defining a new lambda stack


class MyLambdaStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        Function(self, "LambdaFunction",
                 runtime=Runtime.NODEJS_18_X,
                 handler="index.handler",
                 memory_size=1024,
                 timeout=cdk.Duration.seconds(30),
                 code=InlineCode("exports.handler = _ => 'Hello World';")
                 )
