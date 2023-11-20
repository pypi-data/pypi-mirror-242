Library has been developped against python 3.11

## Installation

```bash
pip install py-acli
```

Usage:

```python
import acli.clients.cli as cli
from acli.executors import executor

if __name__ == "__main__":
    # Setup
    client = cli.CliClient(executor=executor("/path/to/acli"))

    # Get Board
    result = client.execute(cli.GetClientInfo())
    print(result)
```
