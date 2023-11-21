# windmill_client

## Overview

`windmill_client` is a Python package designed to interact with the Windmill API. It provides a convenient way to manage jobs, resources, and states within the Windmill environment, offering functionalities like job creation, execution, status tracking, and state management.

It's designed to remain api-compatible with the `wmill` package, but with some added features and a more direct usage
of Windmill's REST API.

## Installation

To install `windmill_client`, run the following command:

```bash
pip install windmill-client
```

## Usage

### Basic Example

Here's a basic example of how to use `windmill_client`:

```python
import windmill_client as wmill

client = wmill.Windmill()

# Create a new job
job_id = client.create_job(path="path/to/script")

# Check job status
status = client.get_job_status(job_id)
print(f"Job Status: {status}")

# run a script synchronously
result = client.run_script(path="path/to/script")
print(f"Script Result: {result}")
```

#### Methods

- `create_job(self, path=None, hash_=None, args=None, scheduled_in_secs=None)`: Create a new job.
- `get_job_status(self, job_id)`: Get the status of a specified job.
- `run_script(self, path=None, hash_=None, args=None, timeout=None, verbose=False, cleanup=True, assert_result_is_not_none=True)`: Run a script synchronously.
- `get_variable(self, path)`: Get a variable from Windmill.
- `set_variable(self, path, value)`: Set a variable in Windmill.
