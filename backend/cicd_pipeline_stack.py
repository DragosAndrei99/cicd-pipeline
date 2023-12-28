import aws_cdk as cdk
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep, ManualApprovalStep
from backend.backend_stack import Backend


class ApiGWHttpApiLambdaDynamodbStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, environment: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        BackendStack = Backend(self, "BackendStack", environment=environment)

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

        dev_stack = ApiGWHttpApiLambdaDynamodbStage(self, "DEV", environment="DEV",
                                        env=cdk.Environment(account="576973527573", region="us-east-1"))
        prod_stack = ApiGWHttpApiLambdaDynamodbStage(self, "PROD", environment="PROD",
                                        env=cdk.Environment(account="576973527573", region="us-east-1"))

        # DEV stage
        dev = pipeline.add_stage(dev_stack)

        # unit tests for infrastructure
        dev.add_pre(ShellStep("Validate-Stack", input=source,
                              commands=["python -m pip install -r requirements.txt",
                                        "python -m pip install pytest",
                                        "python -m pytest tests/unit/test_cicd_pipeline_stack.py"],
                              ))

        # unit tests for application code
        dev.add_pre(ShellStep("Unit-Tests", input=source,
                              commands=["python -m pip install -r requirements.txt",
                                        "python -m pip install pytest",
                                        "python -m pytest tests/unit/test_app.py"],
                              ))

        # e2e tests for API
        dev.add_post(ShellStep('E2E-Tests', commands=["python -m pip install -r requirements.txt",
                                                      f"python tests/e2e/e2e_tests.py"]))

        # PROD stage
        pipeline.add_stage(prod_stack, pre=[ManualApprovalStep("Promote to PROD")])
