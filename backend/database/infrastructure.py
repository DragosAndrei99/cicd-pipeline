import aws_cdk as cdk
import aws_cdk.aws_dynamodb as dynamodb
from constructs import Construct


class Database(Construct):
    def __init__(
        self, scope: Construct, id_: str, env:str, **kwargs
    ):
        super().__init__(scope, id_, **kwargs)

        partition_key = dynamodb.Attribute(
            name="id", type=dynamodb.AttributeType.STRING
        )

        # VPC
        self.vpc = cdk.aws_ec2.Vpc(
            self,
            f"Ingress_{env}",
            cidr="10.1.0.0/16",
            subnet_configuration=[
                cdk.aws_ec2.SubnetConfiguration(
                    name=f"Private-Subnet_{env}", subnet_type=cdk.aws_ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24
                )
            ],
        )

        # Create VPC endpoint
        dynamo_db_endpoint = cdk.aws_ec2.GatewayVpcEndpoint(
            self,
            f"DynamoDBVpce_{env}",
            service=cdk.aws_ec2.GatewayVpcEndpointAwsService.DYNAMODB,
            vpc=self.vpc,
        )

        # Customize the endpoint policy
        dynamo_db_endpoint.add_to_policy(
            cdk.aws_iam.PolicyStatement(
                principals=[cdk.aws_iam.AnyPrincipal()],
                actions=[
                "dynamodb:DescribeStream",
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

        # Create DynamoDB table
        self.dynamodb_table = dynamodb.Table(
            self,
            f"DynamoDBTable_{env}",
            partition_key=partition_key,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )