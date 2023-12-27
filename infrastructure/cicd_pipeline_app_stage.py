import aws_cdk as cdk
from constructs import Construct
from infrastructure.component import Backend

# adding a new custom stage and defining the stack inside it
class ApiGWHttpApiLambdaDynamodbStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        BackendStack = Backend(self, "BackendStack")
