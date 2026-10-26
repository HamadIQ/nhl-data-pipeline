from aws_cdk import (
    # Duration,
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
    aws_iam as iam
    # aws_sqs as sqs,
)
from constructs import Construct

class NhlInfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        
        # Storage Bucket for pipeline outputs
        # Blocks all access to keep net zero costs
        nhl_bucket = s3.Bucket(self, "NHLDataBucket",
            bucket_name="nhl-etl-analytics-dev-storage",
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY  
            )
        # OpenID Connect 
        # Connects with github in a secure trust relationship
        provider = iam.OpenIdConnectProvider.from_open_id_connect_provider_arn(
            self,
            "GitHubProvider",
            open_id_connect_provider_arn=f"arn:aws:iam::{self.account}:oidc-provider/token.actions.githubusercontent.com"
        )
        # Creates a short lived execution role that Github Actions will assume
        # Only trusts tokens originating from this specific repository 
        github_actions_role = iam.Role(
            self,
            "GithubActionsRole",
            role_name="github-actions-nhl-etl-role",
            assumed_by=iam.OpenIdConnectPrincipal(
                provider,
                conditions={
                    "StringEquals":{
                        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
                    },
                    "StringLike":{
                        "token.actions.githubusercontent.com:sub": "repo:*/nhl-data-pipeline:*"
                    }
                }
            )
        )
        
        nhl_bucket.grant_read_write(github_actions_role)