from aws_cdk import core as cdk
from aws_cdk import aws_iam


class NodeApiStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role = aws_iam.Role(
            self,
            "ECSTaskExecutionRole", 
            assumed_by=aws_iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonECSTaskExecutionRolePolicy")],
        )