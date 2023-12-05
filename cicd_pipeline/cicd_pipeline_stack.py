import aws_cdk as cdk
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from cicd_pipeline.cicd_pipeline_app_stage import LambdaAppStage

class MyPipelineStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source = CodePipelineSource.git_hub(
                                "DragosAndrei99/cicd-pipeline",
                                "main",
                                authentication=cdk.SecretValue.secrets_manager("github-key"))

        pipeline =  CodePipeline(self, "Pipeline",
                        pipeline_name="MyPipeline",
                        synth=ShellStep("Synth",
                            input=source,
                            commands=["npm install -g aws-cdk",
                                "python -m pip install -r requirements.txt",
                                "cdk synth"]
                        )
                    )
        # adding the stage to our pipeline
        lambda_function = pipeline.add_stage(LambdaAppStage(self, "CustomStage",
            env=cdk.Environment(account="576973527573", region="us-east-1")))
        
        lambda_function.add_post(ShellStep("validate", input=source,
            commands=["pytest"],
        ))