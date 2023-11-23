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
job_id = client.start_execution(path="path/to/script")

# Check job status
status = client.get_job_status(job_id)
print(f"Job Status: {status}")

# run a script synchronously
result = client.run_script(path="path/to/script")
print(f"Script Result: {result}")
```
