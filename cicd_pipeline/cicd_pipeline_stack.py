import aws_cdk as cdk
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep, ManualApprovalStep
from cicd_pipeline.my_lambda_app.cicd_pipeline_app_stage import MyPipelineAppStage

class MyPipelineStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline =  CodePipeline(self, "Pipeline",
                        pipeline_name="MyPipeline",
                        synth=ShellStep("Synth",
                            input=CodePipelineSource.git_hub(
                                "DragosAndrei99/cicd-pipeline",
                                "main",
                                authentication=cdk.SecretValue.secrets_manager("github-key")),
                            commands=["npm install -g aws-cdk",
                                "python -m pip install -r requirements.txt",
                                "cdk synth"]
                        )
                    )
        
        custom_stage = pipeline.add_stage(MyPipelineAppStage(self, "CustomStage",
            env=cdk.Environment(account="576973527573", region="us-east-1")))
        
        custom_stage.add_post(ManualApprovalStep('approval'))