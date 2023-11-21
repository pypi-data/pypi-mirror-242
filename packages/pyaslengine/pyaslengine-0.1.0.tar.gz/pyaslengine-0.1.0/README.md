# pyaslengine

Python engine for Amazon States Language (ASL) that supports parsing and serialization of definitions, and a local interpreter to run them.

## Installation

```shell
make install
```

## Examples

### Load simple StateMachine definition from local JSON file

```python
import logging

from pyaslengine.data import WorkflowInput
from pyaslengine.workflows import StateMachine

# turn on debug logging
logging.getLogger('pyaslengine').setLevel(logging.DEBUG)

# initialize a state machine by reading a local JSON file
sm = StateMachine.load_definition_file("tests/fixtures/state_machines/do_nothing.json")

# run the state machine by passing an initial payload
results = sm.run(
    workflow_input=WorkflowInput(data={"msg": "in a bottle"})
)
# Out[6]: WorkflowOutput(data={'msg': 'in a bottle'}, context=None)
```

