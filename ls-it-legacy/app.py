import os

from aws_cdk import core as cdk
from aws_cdk import core

from node_api.node_api_stack import NodeApiStack


app = core.App()
NodeApiStack(  
    app,
    "NodeApiStack",
)

app.synth()
