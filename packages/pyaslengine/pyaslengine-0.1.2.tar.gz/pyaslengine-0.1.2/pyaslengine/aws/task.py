"""pyaslengine.aws.task"""

from pyaslengine.log import get_logger

logger = get_logger(__name__)


class AWSTaskInvoker:
    @classmethod
    def invoke(cls, arn, parameters, context, registered_resources):
        if "lambda:invoke" in arn:
            function_arn = parameters["FunctionName"]
            if function_override := registered_resources.get(function_arn):
                return function_override(parameters["Payload"], context)
            return cls._invoke_lambda(function_arn, parameters, context)
        elif "ecs:runTask" in arn:
            # TODO: turn this into marshamallow schema + class
            task_definition = parameters["TaskDefinition"]
            if ecs_task_override := registered_resources.get(task_definition):
                return ecs_task_override(parameters, context)
            return cls._invoke_ecs(parameters)
        elif "sns:publish" in arn:
            topic_arn = parameters["TopicArn"]
            if sns_topic_override := registered_resources.get(topic_arn):
                return sns_topic_override(parameters, context)
            return cls._invoke_sns(parameters)
        else:
            raise NotImplementedError(
                f"Some AWS services not yet supported, cannot invoke: {arn}"
            )

    @classmethod
    def _invoke_lambda(cls, function_arn, parameters, context):
        import boto3
        import json

        lambda_client = boto3.client("lambda")
        payload = parameters["Payload"]
        response = lambda_client.invoke(
            FunctionName=function_arn,
            InvocationType="RequestResponse",
            Payload=json.dumps(payload),
            # ClientContext=json.dumps(context),  # TODO: uncomment and enable
        )
        payload_response = json.loads(response["Payload"].read().decode("utf-8"))
        return {"Payload": payload_response}

    @classmethod
    def _invoke_ecs(cls, parameters):
        import boto3
        import time

        ecs_client = boto3.client("ecs")
        cluster = parameters["Cluster"]
        task_definition = parameters["TaskDefinition"]
        subnets = parameters["NetworkConfiguration"]["AwsvpcConfiguration"]["Subnets"]
        security_groups = parameters["NetworkConfiguration"]["AwsvpcConfiguration"][
            "SecurityGroups"
        ]

        # NOTE: this is only problematic for serialization purposes...
        #   with a proper marshmallow schema, this and above could be removed
        if len(parameters["Overrides"]["ContainerOverrides"]) > 1:
            raise NotImplementedError(
                "Currently only one container per ECS task is supported"
            )
        container_name = parameters["Overrides"]["ContainerOverrides"][0]["Name"]
        container_command = parameters["Overrides"]["ContainerOverrides"][0]["Command"]

        response = ecs_client.run_task(
            cluster=cluster,
            launchType="FARGATE",
            taskDefinition=task_definition,
            networkConfiguration={
                "awsvpcConfiguration": {
                    "subnets": subnets,
                    "securityGroups": security_groups,
                    "assignPublicIp": "ENABLED",
                }
            },
            overrides={
                "containerOverrides": [
                    {
                        "name": container_name,
                        "command": container_command,
                    },
                ],
            },
        )

        if response.get("tasks"):
            task_arn = response["tasks"][0]["taskArn"]
            while True:
                describe_response = ecs_client.describe_tasks(
                    cluster=cluster, tasks=[task_arn]
                )
                task_status = describe_response["tasks"][0]["lastStatus"]
                logger.info(f"ECS TASK STATUS: {task_status}")
                if task_status == "STOPPED":
                    break
                time.sleep(10)
            logger.debug(f"Task {task_arn} has completed.")
        else:
            logger.debug("Failed to start task.")

        if response.get("failures"):
            logger.error(f"Failures: {response['failures']}")
            raise RuntimeError("ECS task failed with errors")

    @classmethod
    def _invoke_sns(cls, parameters):
        logger.warning("SNS not yet supported, but not raising, returning {}")
        return {}
