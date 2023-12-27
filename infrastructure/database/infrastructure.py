import aws_cdk as cdk
import aws_cdk.aws_dynamodb as dynamodb
from constructs import Construct


class Database(Construct):
    def __init__(
        self, scope: Construct, id_: str, *, dynamodb_billing_mode: dynamodb.BillingMode
    ):
        super().__init__(scope, id_)

        partition_key = dynamodb.Attribute(
            name="id", type=dynamodb.AttributeType.STRING
        )

        # VPC
        self.vpc = cdk.aws_ec2.Vpc(
            self,
            "Ingress",
            cidr="10.1.0.0/16",
            subnet_configuration=[
                cdk.aws_ec2.SubnetConfiguration(
                    name="Private-Subnet", subnet_type=cdk.aws_ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24
                )
            ],
        )
        
        # Create VPC endpoint
        dynamo_db_endpoint = cdk.aws_ec2.GatewayVpcEndpoint(
            self,
            "DynamoDBVpce",
            service=cdk.aws_ec2.GatewayVpcEndpointAwsService.DYNAMODB,
            vpc=self.vpc,
        )

        # This allows to customize the endpoint policy
        dynamo_db_endpoint.add_to_policy(
            cdk.aws_iam.PolicyStatement(  # Restrict to listing and describing tables
                principals=[cdk.aws_iam.AnyPrincipal()],
                actions=[                "dynamodb:DescribeStream",
                "dynamodb:DescribeTable",
                "dynamodb:Get*",
                "dynamodb:Query",
                "dynamodb:Scan",
                "dynamodb:CreateTable",
                "dynamodb:Delete*",
                "dynamodb:Update*",
                "dynamodb:PutItem"],
                resources=["*"],
            )
        )

        self.dynamodb_table = dynamodb.Table(
            self,
            "DynamoDBTable",
            billing_mode=dynamodb_billing_mode,
            partition_key=partition_key,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )