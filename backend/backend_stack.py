
from typing import Any

import aws_cdk as cdk
from constructs import Construct

from backend.api.infrastructure import API
from backend.database.infrastructure import Database


class Backend(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        **kwargs: Any,
    ):
        super().__init__(scope, id_, **kwargs)

        database = Database(
            self,
            "Database",
        )

        api = API(
            self,
            "API",
            dynamodb_table_name=database.dynamodb_table.table_name,
            vpc=database.vpc
        )

        database.dynamodb_table.grant_read_write_data(api.api_handler)

        # self.api_endpoint = cdk.CfnOutput(
        #     self,
        #     "APIEndpoint",
        #     # API doesn't disable create_default_stage, hence URL will be defined
        #     value=api.api_gateway_http_api.url,  # type: ignore
        # )