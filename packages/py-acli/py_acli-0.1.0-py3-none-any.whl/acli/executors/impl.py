import subprocess
from dataclasses import dataclass
from io import StringIO
from typing import Any

import pandas as pd

from acli.base.args import remove_arg_and_value
from acli.base.spec import Command, Executor


def executor(executable, with_vars=True, with_dataframes=True):
    e = SubprocessExecutor(executable)
    if with_vars:
        e = WithVars(e)
    if with_dataframes:
        e = WithDataFrames(e)
    return e


@dataclass
class RunCommand(Command):
    @staticmethod
    def action() -> str:
        return "run"


class WithVars(Executor):
    _delegate: Executor

    def __init__(self, delegate: Executor):
        super().__init__(delegate.context)
        self._delegate = delegate

    def execute(self, command: Command, site: str | None, args: list[str]) -> str:
        if not command.has_replacement_vars():
            return self._delegate.execute(command, site, args)

        delegate_command_args = [
            self.sanitize_arg_str(arg) if " " in arg else arg for arg in args
        ]
        delegate_command: str = " ".join(
            ["--action", command.action(), *delegate_command_args]
        )
        get_vars_command: str = "--action getReplacementVariableList"
        run_command_args = ["-i", delegate_command, "-i", get_vars_command]

        result = self._delegate.execute(RunCommand(), site, run_command_args)

        if not isinstance(result, str):
            return result

        # Split the output into the two parts
        command_outputs: list[str] = list(
            WithVars.separate_run_outputs(result).values()
        )
        if len(command_outputs) < 2:
            return result

        # The first part is the output of the run command,
        # the second part is the output of the getReplacementVariableList command
        last_output = command_outputs[-1]
        for record in parse_csv_dataframe(last_output).to_dict(orient="records"):
            self.context[record["Name"]] = self.as_value(record["Value"])

        return "\n".join(command_outputs[:-1])

    @staticmethod
    def as_value(s: str) -> Any:
        try:
            return int(s)
        except ValueError:
            return s

    @staticmethod
    def separate_run_outputs(output: str) -> dict[str, str]:
        """A run output starts with a line Run:,
        then all lines until the next Run: are part of the output"""
        lines = str.split(output, "\n")
        outputs: dict[str, list[str]] = {"none": []}
        current_run = "none"
        for line in lines:
            if line.startswith("Run:"):
                current_run = line[4:].strip()
                outputs[current_run] = []
            else:
                outputs[current_run].append(line)
        return {
            command: "\n".join(lines)
            for command, lines in outputs.items()
            if command != "none"
        }

    @staticmethod
    def sanitize_arg_str(s: str) -> str:
        # Replace all " by ""
        # if s contains space or a ' then surround with "
        if " " in s or "'" in s:
            return '"' + s.replace('"', '""') + '"'
        else:
            return s


class WithDataFrames(Executor):
    def __init__(self, delegate: Executor):
        super().__init__(delegate.context)
        self._delegate = delegate

    def execute(
        self, command: Command, site: str | None, args: list[str]
    ) -> pd.DataFrame | str:
        if self.may_be_convertible_to_dataframe(command):
            self.set_html_output_type(args)

            result = self._delegate.execute(command, site, args)
            if isinstance(result, str):
                # Fix ACLI bug that outputs first row as table header in HTML
                bad_header = command.action().startswith(
                    "get"
                ) and not command.action().endswith("List")
                return parse_html_dataframe(result, fix_bad_header=bad_header)
            else:
                return result
        else:
            return self._delegate.execute(command, site, args)

    @staticmethod
    def set_html_output_type(args):
        remove_arg_and_value(args, "--outputType")
        args.append("--outputType")
        args.append("html")

    @staticmethod
    def may_be_convertible_to_dataframe(command):
        return command.action().startswith("get") and command.supports_output_type()


def parse_html_dataframe(s: str, fix_bad_header=False) -> pd.DataFrame | str:
    try:
        df = try_parse_html_dataframe(s)
        if fix_bad_header and isinstance(df, pd.DataFrame):
            df = _fix_dataframe_header(df)
        return df
    except ValueError:
        print("Failed to parse as html, falling back to raw")
        return s


def _fix_dataframe_header(df: pd.DataFrame) -> pd.DataFrame:
    if len(df.columns) != 2:
        return df
    dg = pd.read_csv(StringIO(df.to_csv(index=False)), header=None)
    dg.rename(columns={0: "Key", 1: "Value"}, inplace=True)
    return dg


def try_parse_html_dataframe(s: str) -> pd.DataFrame | str:
    lines = str.split(s, "\n")
    non_empty_lines = [line for line in lines if line.strip()]
    html_lines = [
        line for line in non_empty_lines if line.strip().startswith("<")
    ]  # Very naive
    if len(html_lines) > 0:
        return pd.read_html(
            StringIO("\n".join(html_lines)), keep_default_na=False, encoding="utf-8"
        )[0]
    elif len(non_empty_lines) == 1 and non_empty_lines[0].startswith("0 "):
        return pd.DataFrame()
    else:
        # Seems not html, fallback to the original string
        return s


def parse_csv_dataframe(s: str) -> pd.DataFrame:
    lines = str.split(s, "\n")
    csv_lines = [line for line in lines if line.startswith('"')]  # Very naive
    if csv_lines:
        return pd.read_csv(StringIO("\n".join(csv_lines)), keep_default_na=False)
    else:
        return pd.DataFrame()


class SubprocessExecutor(Executor):
    def __init__(self, executable="ad"):
        super().__init__()
        self.executable = executable

    def execute(self, command: Command, site: str | None, args: list[str]) -> str:
        if site:
            command_line = [self.executable, site, "-a", command.action(), *args]
        else:
            command_line = [self.executable, "-a", command.action(), *args]
        try:
            print("Executing command: ", " ".join(command_line), "...")
            result = subprocess.run(
                command_line, check=True, text=True, capture_output=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(e.stderr)
            raise e
