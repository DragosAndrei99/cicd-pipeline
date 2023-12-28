import aws_cdk as cdk
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from backend.backend_stack import Backend

class ApiGWHttpApiLambdaDynamodbStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        BackendStack = Backend(self, "BackendStack")

class MyPipelineStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source = CodePipelineSource.git_hub(
            "DragosAndrei99/cicd-pipeline",
            "main",
            authentication=cdk.SecretValue.secrets_manager("github-key"))

        pipeline = CodePipeline(self, "Pipeline",
                                pipeline_name="MyPipeline",
                                synth=ShellStep("Synth",
                                                input=source,
                                                commands=["npm install -g aws-cdk",
                                                          "python -m pip install -r requirements.txt",
                                                          "cdk synth"]
                                                )
                                        )
        # adding the app stage to our pipeline
        app = pipeline.add_stage(ApiGWHttpApiLambdaDynamodbStage(self, "ApiGWHttpApiLambdaDynamodbStage",
                                                            env=cdk.Environment(account="576973527573", region="us-east-1")))

        # unit tests for infrastructure
        app.add_pre(ShellStep("Validate-Stack", input=source,
                                          commands=["python -m pip install -r requirements.txt",
                                                    "python -m pip install pytest",
                                                    "python -m pytest tests/unit/test_cicd_pipeline_stack.py"],
                                          ))

        # unit tests for application code
        app.add_pre(ShellStep("Unit-Tests", input=source,
                                          commands=["python -m pip install -r requirements.txt",
                                                    "python -m pip install pytest",
                                                    "python -m pytest tests/unit/test_app.py"],
                                          ))

        # add manual approval step 
        # add notification ?
        # return the api gw url
        # add e2e tests using bash with curl command
