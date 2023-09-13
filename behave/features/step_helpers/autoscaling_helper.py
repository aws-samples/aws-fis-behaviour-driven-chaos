import logging

logger = logging.getLogger(__name__)


def get_asg_details(client, target_asg_tag: str, asgs_to_return: int) -> list:
    """
    Return details of ASGs matching the target tag

    If asgs_to_return is '0', then return all the matching ASGs,
    otherwise, return the number requested. If more are requested
    than exist, then all available will be returned.
    """

    tag_name = target_asg_tag.split(":")[0]
    tag_value = target_asg_tag.split(":")[1]

    logger.info(
        f"Looking for ASGs with tag name: {tag_name} and tag value: {tag_value}"
    )

    paginator = client.get_paginator("describe_auto_scaling_groups")

    page_iterator = paginator.paginate(
        Filters=[{"Name": f"tag:{tag_name}", "Values": [tag_value]}]
    )

    asg_list = []
    for page in page_iterator:
        asg_list.extend(page["AutoScalingGroups"])

    if asgs_to_return == 0:
        return asg_list
    else:
        return asg_list[0:asgs_to_return]
