import aws_cdk as cdk
from backend.backend_stack import Backend


def test_app_handler():

    # GIVEN
    app = cdk.App()

    # WHEN
    Backend(app, 'Stack', environment="DEV")

    # THEN
    template = app.synth().get_stack_by_name('Stack').template
    functions = [resource for resource in template['Resources'].values()
                 if resource['Type'] == 'AWS::Lambda::Function']

    assert len(functions) == 4
    assert functions[0]['Properties']['MemorySize'] == 1024