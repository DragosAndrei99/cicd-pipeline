import aws_cdk as cdk
from stacks.cicd_pipeline_lambda_stack import MyLambdaStack


def test_lambda_handler():

    # GIVEN
    app = cdk.App()

    # WHEN
    MyLambdaStack(app, 'Stack')

    # THEN
    template = app.synth().get_stack_by_name('Stack').template
    functions = [resource for resource in template['Resources'].values()
                 if resource['Type'] == 'AWS::Lambda::Function']

    assert len(functions) == 1
    assert functions[0]['Properties']['MemorySize'] == 1024
    assert functions[0]['Properties']['Timeout'] == 30
