from enum import StrEnum
from typing import Any
from pydantic import validate_call

class ComparisonOperator(StrEnum):
    """
    Numerical comparison operators
    """

    EQUALS = "="
    NOT_EQUALS = "!="
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL_TO = ">="
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL_TO = "<="

def try_convert_to_number(value: Any) -> int | float | None:
    """
    Try to convert a value to a number

    Args:
        value (Any): The value to convert

    Returns:
        int | float | None: The converted value, or None if the value could not be converted
    """
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return None

@validate_call
def value_comparison(value1: Any, value2: Any, comparison_operator: ComparisonOperator, to_number_size_comparsion: bool = False) -> bool:
    """
    Compare two values using a specified comparison operator

    Args:
        value1 (Any): The first value to compare
        value2 (Any): The second value to compare
        comparison_operator (ComparisonOperator): The comparison operator to use

    Returns:
        bool: True if the comparison is true, False otherwise
    """
    match comparison_operator:
        case ComparisonOperator.EQUALS:
            return value1 == value2
        case ComparisonOperator.NOT_EQUALS:
            return value1 != value2
        case _:
            # Number comparison
            if to_number_size_comparsion:
                value1 = try_convert_to_number(value1)
                value2 = try_convert_to_number(value2)
            match comparison_operator:
                case ComparisonOperator.GREATER_THAN:
                    return value1 > value2
                case ComparisonOperator.GREATER_THAN_OR_EQUAL_TO:
                    return value1 >= value2
                case ComparisonOperator.LESS_THAN:
                    return value1 < value2
                case ComparisonOperator.LESS_THAN_OR_EQUAL_TO:
                    return value1 <= value2
                case _:
                    raise ValueError(f"Invalid comparison operator: {comparison_operator}")