from typing import Any


def parse_config_address(key_address: str, value: Any):
    """Convert a string address and its value to a dictionary."""

    base_dict = {}
    current_nested_dict = base_dict
    dict_keys = key_address.split(".")
    last_dict_key = dict_keys.pop()

    for index, dict_key in enumerate(dict_keys, 1):
        current_nested_dict = current_nested_dict.setdefault(dict_key, dict())

    current_nested_dict[last_dict_key] = value

    return base_dict
