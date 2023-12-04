#!/usr/bin/env python3
import aws_cdk as cdk
from cicd_pipeline.cicd_pipeline_stack import MyPipelineStack

app = cdk.App()
MyPipelineStack(app, "MyPipelineStack",
    env=cdk.Environment(account="111111111111", region="eu-west-1")
)

app.synth()