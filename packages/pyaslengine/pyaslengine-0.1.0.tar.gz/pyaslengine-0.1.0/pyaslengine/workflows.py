"""pyaslengine.workflows"""

import json
import re

from attrs import define, field

from pyaslengine.log import get_logger
from pyaslengine.data import (
    Context,
    WorkflowInput,
    WorkflowOutput,
    StateInput,
    StateOutput,
    JSON,
)
from pyaslengine.states import (
    State,
    Choice,
    Task,
    Map,
    Fail,
    Succeed,
    Pass,
    Wait,
    Parallel,
)

logger = get_logger(__name__)


@define
class Workflow:
    comment: str = field(default=None)
    start_at: str = field(default=None)
    states: dict[str, State] = field(default=None)

    @classmethod
    def load_definition_file(cls, definition_filepath) -> "StateMachine":
        from pyaslengine.schemas import StateMachineSchema

        with open(definition_filepath) as f:
            return StateMachineSchema().load(json.load(f))

    @classmethod
    def load_aws_arn(cls, step_function_arn) -> "StateMachine":
        # TODO: break into plugin architecture
        import boto3
        from pyaslengine.schemas import StateMachineSchema

        client = boto3.client("stepfunctions")
        response = client.describe_state_machine(stateMachineArn=step_function_arn)
        state_machine_definition = response["definition"]
        return StateMachineSchema().load(json.loads(state_machine_definition))

    def to_dict(self):
        from pyaslengine.schemas import StateMachineSchema

        return StateMachineSchema().dump(self)

    def to_json(self, indent: int = None):
        return json.dumps(self.to_dict(), indent=indent)

    def get_state(self, state_id):
        return self.states[state_id]

    def process_input_payload(
        self,
        state_input: StateInput,
        current_state: State,
    ) -> tuple[StateInput, JSON]:
        """Process input payload for State work.

        Order of application:
            - InputPath
            - Parameters
        """
        # apply InputPath
        state_input.data = state_input.apply_input_path(current_state.input_path)
        original_data = state_input.data

        # apply Parameters
        if isinstance(current_state, (Task, Parallel, Map, Pass)):
            state_input.data = state_input.apply_parameters(current_state.parameters)

        return state_input, original_data

    def process_output_payload(
        self,
        state_output: StateOutput,
        current_state: State,
        original_data: JSON,
    ) -> StateOutput:
        """Process output payload for State return.

        Order of application:
            - ResultSelector
            - ResultPath
            - OutputPath
        """
        # apply ResultSelector
        state_output.data = state_output.apply_result_selector(
            current_state.result_selector
        )

        # apply ResultPath
        state_output.data = state_output.apply_result_path(
            current_state.result_path,
            state_output.data,
            original_data,
        )

        # apply OutputPath
        state_output.data = state_output.apply_output_path(current_state.output_path)

        return state_output

    def run(
        self,
        workflow_input: WorkflowInput,
        registered_resources: dict | None = None,
        context: Context = None,
    ) -> WorkflowOutput:
        """Run Workflow"""
        # initialize new Context if not provided
        if not context:
            context = Context.create(self, workflow_input)

        # initialize first state and input for Workflow
        state_input = StateInput(data=workflow_input.data, context=context)
        current_state_id = self.start_at
        logger.info(f"Workflow Start At: '{current_state_id}'")
        logger.info(f"Workflow Input: '{state_input}'")

        while True:
            # update context
            context.set_current_state(current_state_id)
            state_input.context = context

            # handle no next state
            if current_state_id is None:
                logger.warning(
                    "Next step undefined, exiting.  Consider explicit Succeed or Fail "
                    "state."
                )
                return WorkflowOutput(data=state_input.data)

            current_state = self.get_state(current_state_id)
            logger.info(f"Current State: '{current_state_id}' / {current_state}")
            logger.info(f"State Input: {state_input}")

            # process Input Payload
            state_input, original_data = self.process_input_payload(
                state_input, current_state
            )

            logger.info(f"Processing State: '{current_state_id}'")

            # CHOICE
            if isinstance(current_state, Choice):
                next_state_id, state_output = current_state.run(state_input)

            # TASK
            elif isinstance(current_state, Task):
                next_state_id, state_output = current_state.run(
                    state_input, registered_resources=registered_resources
                )

            # MAP
            elif isinstance(current_state, Map):
                next_state_id, state_output = current_state.run(
                    state_input,
                    registered_resources=registered_resources,
                    context=context,
                )

            # PARALLEL
            elif isinstance(current_state, Parallel):
                next_state_id, state_output = current_state.run(
                    state_input, registered_resources=registered_resources
                )

            # PASS
            elif isinstance(current_state, Pass):
                next_state_id, state_output = current_state.run(state_input)

            # WAIT
            elif isinstance(current_state, Wait):
                state_output = current_state.run(state_input)
                next_state_id = current_state.next

            # FAIL
            elif isinstance(current_state, Fail):
                logger.warning("Fail state encountered, not fully implemented, exiting")
                return WorkflowOutput(data=state_input.data)

            # SUCCEED
            elif isinstance(current_state, Succeed):
                return WorkflowOutput(data=state_input.data)

            else:
                raise Exception(f"State type: {current_state.type} not recognized")

            # process Output Payload
            state_output = self.process_output_payload(
                state_output, current_state, original_data
            )

            # continue workflow state loop
            logger.info(f"State Output: {state_output}")
            state_input = state_output.to_state_input()
            current_state_id = next_state_id


@define
class StateMachine(Workflow):
    pass


@define
class Iterator(Workflow):
    processor_config: dict = field(default=None)
    pass


class TaskInvoker:
    def __init__(self, resources: dict = None):
        self._resource_callable_map = {}
        if resources:
            for k, v in resources.items():
                self.register(k, v)

    def register(self, resource_identifier, callable):
        self._resource_callable_map[resource_identifier] = callable

    def invoke(self, task, parameters: JSON, context: JSON):
        resource_identifier = task.resource
        callable = self._resource_callable_map.get(resource_identifier)
        if callable:
            return callable(parameters, context)
        if self._is_aws_arn(resource_identifier):
            return self._invoke_aws_arn(resource_identifier, parameters, context)
        raise ValueError(f"No strategies for invoking resource: {resource_identifier}")

    def _is_aws_arn(self, resource):
        return re.match(r"^arn:aws", resource)

    def _invoke_aws_arn(self, arn, parameters, context):
        # TODO: invoke this logic
        if "lambda:invoke" in arn:
            function_arn = parameters["FunctionName"]
            response = self._invoke_lambda(function_arn, parameters, context)
            return response
        elif "ecs:runTask" in arn:
            # TODO: turn this into marshamallow schema + class
            return self._invoke_ecs(parameters)
        elif "sns:publish" in arn:
            return self._invoke_sns(parameters)
        else:
            raise NotImplementedError(
                f"Some AWS services not yet supported, cannot invoke: {arn}"
            )

    def _invoke_lambda(self, function_arn, parameters, context):
        import boto3
        import json

        lambda_client = boto3.client("lambda")
        payload = parameters["Payload"]
        response = lambda_client.invoke(
            FunctionName=function_arn,
            InvocationType="RequestResponse",
            Payload=json.dumps(payload),
        )
        payload_response = json.loads(response["Payload"].read().decode("utf-8"))
        return {"Payload": payload_response}

    def _invoke_ecs(self, parameters):
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

    def _invoke_sns(self, parameters):
        logger.warning("SNS not yet supported, but not raising, returning {}")
        return {}
