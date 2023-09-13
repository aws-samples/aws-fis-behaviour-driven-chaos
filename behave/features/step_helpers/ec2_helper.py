def get_instance_details(client, instance_ids: list) -> list:
    """
    Return the details of the instances
    """

    paginator = client.get_paginator("describe_instance_status")

    page_iterator = paginator.paginate(InstanceIds=instance_ids)

    instance_list = []
    for page in page_iterator:
        instance_list.extend(page["InstanceStatuses"])

    return instance_list
