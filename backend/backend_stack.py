
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
        environment: str,
        **kwargs: Any,
    ):
        super().__init__(scope, id_, **kwargs)

        database = Database(
            self,
            "Database",
            env=environment
        )

        api = API(
            self,
            "API",
            dynamodb_table_name=database.dynamodb_table.table_name,
            vpc=database.vpc,
            env=environment
        )
        database.dynamodb_table.grant_read_data(api.scan_lambda_handler)
        database.dynamodb_table.grant_write_data(api.post_lambda_handler)
        database.dynamodb_table.grant_write_data(api.update_lambda_handler)
        database.dynamodb_table.grant_write_data(api.delete_lambda_handler)

        self.api_gw_url = cdk.CfnOutput(self, "apiUrl", value=api.url)