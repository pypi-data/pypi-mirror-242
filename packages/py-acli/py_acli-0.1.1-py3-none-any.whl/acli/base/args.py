from typing import Any


def to_cli_args_array(command: dict[str, Any]) -> list[str]:
    def _collect_args(
        field_name, field_value, multi_allowed, collected: list[str]
    ) -> None:
        if field_value is None:
            return
        elif isinstance(field_value, dict):
            for fn, fv in field_value.items():
                _collect_args(fn, fv, False, collected)
        elif isinstance(field_value, list):
            for fv in field_value:
                _collect_args(field_name, fv, True, collected)
        else:
            flag = _format_flag(field_name)
            if flag in collected and not multi_allowed:
                raise ValueError(f"Duplicate flag {flag}")
            if field_value:
                collected.append(_format_flag(field_name))
            if isinstance(field_value, str):
                collected.append(_format_value(field_value))

    def _format_flag(field_name):
        return f"--{_snake_to_camel_case(field_name)}"

    def _format_value(field_value):
        return field_value

    # Flatten this to a dict of args, and recursively enter into any sub-objects
    cli_flags: list[str] = []
    for k, v in command.items():
        _collect_args(k, v, False, cli_flags)

    return cli_flags


def _snake_to_camel_case(s: str) -> str:
    """Transforms a snake_case string to a camelCase string"""
    join = "".join(word.capitalize() for word in s.split("_"))
    return join[0].lower() + join[1:]


def remove_arg_and_value(args: list[str], arg: str) -> list[str]:
    pos = find_arg_pos(args, arg)
    if pos is None:
        return args
    else:
        return args[:pos] + args[pos + 2 :]


def find_arg_pos(args, arg) -> int | None:
    for i, a in enumerate(args):
        if a == arg:
            return i
    return None
