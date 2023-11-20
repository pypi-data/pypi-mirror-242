from dataclasses import dataclass, asdict
from typing import Any

from acli.base.args import to_cli_args_array


@dataclass
class Command:
    @staticmethod
    def action() -> str:
        raise NotImplementedError()

    @staticmethod
    def has_replacement_vars() -> bool:
        return False

    @staticmethod
    def supports_output_type() -> bool:
        return False


class Executor:
    context: dict[str, Any]

    def __init__(self, context: dict[str, Any] | None = None):
        self.context = {} if context is None else context

    def execute(self, command: Command, site: str | None, args: list[str]) -> Any:
        ...


@dataclass
class Client:
    executor: Executor

    @property
    def context(self):
        return self.executor.context

    def do_execute(self, command):
        command_line = to_cli_args_array(asdict(command))
        if self.executor:
            return self.executor.execute(command, None, command_line)
        else:
            return "No executor configured"


@dataclass
class RemoteClient(Client):
    site: str

    def do_execute(self, command):
        command_line = to_cli_args_array(asdict(command))
        if self.executor:
            return self.executor.execute(command, self.site, command_line)
        else:
            return "No executor configured"
