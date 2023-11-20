from typing import Any


def export_vars(context: dict[str, Any], target: dict[str, Any]):
    for k, v in context.items():
        target[k] = v
