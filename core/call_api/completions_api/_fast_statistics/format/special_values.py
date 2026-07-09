from typing import Any

def format_special_values(value: Any) -> str:
    if value is None:
        return "No Set"
    elif isinstance(value, bool):
        return "Enabled" if value else "Disabled"
    else:
        return str(value)