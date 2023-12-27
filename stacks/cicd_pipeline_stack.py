import aws_cdk as cdk
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from stacks.cicd_pipeline_app_stage import ApiGWHttpApiLambdaDynamodbStage
import aws_cdk.aws_iam as iam


class MyPipelineStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role = iam.Role(self, "Role",
          assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com")) # required

        role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=["*"],
            actions=["ec2:DescribeAvailabilityZones"]
        ))
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
                                                ),
                                role=role
                                )
        # adding the stage to our pipeline
        lambda_function = pipeline.add_stage(ApiGWHttpApiLambdaDynamodbStage(self, "ApiGWHttpApiLambdaDynamodbStage",
                                                            env=cdk.Environment(account="576973527573", region="us-east-1")))

        # adding test step to be ran before any of the stacks in this stage
        lambda_function.add_pre(ShellStep("ValidateStack", input=source,
                                          commands=["python -m pip install -r requirements.txt",
                                                    "python -m pip install pytest",
                                                    "python -m pytest"],
                                          ))
