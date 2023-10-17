from __future__ import annotations
import typing as t

ConfigDict = dict[str, t.Union[str, "ConfigDict"]]


def parse_config_address(key_address: str, value: str) -> ConfigDict:
    """Convert a string address and its value to a dictionary."""

    base_dict: ConfigDict = {}
    current_nested_dict = base_dict  # type: ignore
    dict_keys = key_address.split(".")
    last_dict_key = dict_keys.pop()

    for dict_key in dict_keys:
        current_nested_dict: ConfigDict = current_nested_dict.setdefault(  # type: ignore
            dict_key, dict()
        )

    current_nested_dict[last_dict_key] = value

    return base_dict
