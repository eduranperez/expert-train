from aws_cdk import core as cdk
from aws_cdk import aws_iam
from aws_cdk import aws_ecs
from aws_cdk import aws_ecr


class NodeApiStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role = aws_iam.Role(
            self,
            "ECSTaskExecutionRole", 
            assumed_by=aws_iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonECSTaskExecutionRolePolicy")],
        )
        task = aws_ecs.FargateTaskDefinition(
            self,
            "node-api",
            cpu=256,
            memory_limit_mib=512,
            execution_role=role,
            family="node-api")

        image = aws_ecs.ContainerImage.from_registry("094700089952.dkr.ecr.us-west-2.amazonaws.com/node-api:v1")
        task.add_container(
            "node-api",
            image=image,
            cpu=256,
            memory_limit_mib=512,
            port_mappings=[aws_ecs.PortMapping(container_port=3000,host_port=3000)],
            logging=aws_ecs.LogDriver.aws_logs(stream_prefix="node-api")
        )

