import aws_cdk as core
import aws_cdk.assertions as assertions

from nhl_infra.nhl_infra_stack import NhlInfraStack

# example tests. To run these tests, uncomment this file along with the example
# resource in nhl_infra/nhl_infra_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = NhlInfraStack(app, "nhl-infra")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
