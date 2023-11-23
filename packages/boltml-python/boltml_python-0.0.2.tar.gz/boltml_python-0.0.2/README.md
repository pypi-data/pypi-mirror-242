# boltml-python
The [BoltML](https://boltml.dev/) client library for Python.

## Installation
Install the latest version of the BoltML client library using pip:

```bash
pip install boltml-python
```

## Usage
After signing up for BoltML, you will receive a client token. You can use this token to authenticate with the BoltML API.

```python
from boltml import BoltMLClient

API_ENDPOINT = "https://api.boltml.dev"
CLIENT_TOKEN = "<...>"

client = BoltMLClient(API_ENDPOINT, CLIENT_TOKEN)
```
