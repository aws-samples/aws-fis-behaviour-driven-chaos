import boto3


def create_client(service: str, context):
    """
    create a boto client object and store it in the context
    for later use
    """

    context.clients[service] = boto3.client(
        service, region_name=context.config.userdata["aws_region"]
    )
