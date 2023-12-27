import aws_cdk as cdk
from infrastructure.cicd_pipeline_app_stack import ApiGWHttpApiLambdaDynamodbStack


def test_app_handler():

    # GIVEN
    app = cdk.App()

    # WHEN
    ApiGWHttpApiLambdaDynamodbStack(app, 'Stack')

    # THEN
    template = app.synth().get_stack_by_name('Stack').template
    functions = [resource for resource in template['Resources'].values()
                 if resource['Type'] == 'AWS::Lambda::Function']

    assert len(functions) == 1
    assert functions[0]['Properties']['MemorySize'] == 1024