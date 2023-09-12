import logging
from step_helpers.autoscaling_helper import get_asg_details
from step_helpers.clients import create_client
from step_helpers.ec2_helper import get_instance_details

logger = logging.getLogger(__name__)


@step("I have an EC2 Auto-Scaling Group with at least {number} running EC2 instances")
def step_impl(context, number):

    if "autoscaling" not in context.clients:
        create_client("autoscaling", context)

    if "ec2" not in context.clients:
        create_client("ec2", context)

    # our environment only has 1 ASG with the target tag so get the first asg matching the target tag
    asg_list = get_asg_details(
        context.clients["autoscaling"], context.config.userdata["target_tag"], 1
    )

    # get all the in_service instances
    in_service_instances = [
        instance["InstanceId"]
        for asg in asg_list
        for instance in asg["Instances"]
        if instance["LifecycleState"] == "InService"
    ]

    instance_details = get_instance_details(
        context.clients["ec2"], in_service_instances
    )

    # make sure the instances are in the running state
    running_instances = [
        instance["InstanceId"]
        for instance in instance_details
        if instance["InstanceState"]["Name"] == "running"
    ]

    logger.info(
        f"number of running instances is: {len(running_instances)}, wanted: {number}"
    )

    assert len(running_instances) >= int(number)


@step(
    "I have an EC2 Auto-Scaling Group with instances distributed across at least {number} Availability Zones"
)
def step_impl(context, number):

    if "autoscaling" not in context.clients:
        create_client("autoscaling", context)

    if "ec2" not in context.clients:
        create_client("ec2", context)

    # our environment only has 1 ASG with the target tag so get the first asg matching the target tag
    asg_list = get_asg_details(
        context.clients["autoscaling"], context.config.userdata["target_tag"], 1
    )

    # get all the in_service instances
    in_service_instances = [
        instance["InstanceId"]
        for asg in asg_list
        for instance in asg["Instances"]
        if instance["LifecycleState"] == "InService"
    ]

    instance_details = get_instance_details(
        context.clients["ec2"], in_service_instances
    )

    # make sure the instances are in the running state and return a set of unique AZ's
    azs = {
        instance["AvailabilityZone"]
        for instance in instance_details
        if instance["InstanceState"]["Name"] == "running"
    }

    logger.info(
        f"number of AZs with EC2 instances is: {len(azs)}, wanted: {number}. AZ distribution is {azs}"
    )

    assert len(azs) >= int(number)
