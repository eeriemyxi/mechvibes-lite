from typing import Any


def parse_config_address(key_address: str, value: Any) -> dict[str, Any]:
    """Convert a string address and its value to a dictionary."""

    base_dict: dict[str, Any] = {}
    current_nested_dict = base_dict
    dict_keys = key_address.split(".")
    last_dict_key = dict_keys.pop()

    for dict_key in dict_keys:
        current_nested_dict = current_nested_dict.setdefault(dict_key, dict())

    current_nested_dict[last_dict_key] = value

    return base_dict
