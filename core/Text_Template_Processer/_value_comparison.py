from enum import StrEnum
from typing import Any

class NumericalComparison(StrEnum):
    """
    Numerical comparison operators
    """

    EQUALS = "="
    NOT_EQUALS = "!="
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL_TO = ">="
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL_TO = "<="

def value_comparison(value1: Any, value2: Any, comparison_operator: NumericalComparison) -> bool:
    """
    Compare two values using a specified comparison operator

    Args:
        value1 (Any): The first value to compare
        value2 (Any): The second value to compare
        comparison_operator (NumericalComparison): The comparison operator to use

    Returns:
        bool: True if the comparison is true, False otherwise
    """
    match comparison_operator:
        case NumericalComparison.EQUALS:
            return value1 == value2
        case NumericalComparison.NOT_EQUALS:
            return value1 != value2
        case NumericalComparison.GREATER_THAN:
            return value1 > value2
        case NumericalComparison.GREATER_THAN_OR_EQUAL_TO:
            return value1 >= value2
        case NumericalComparison.LESS_THAN:
            return value1 < value2
        case NumericalComparison.LESS_THAN_OR_EQUAL_TO:
            return value1 <= value2
        case _:
            raise ValueError(f"Invalid comparison operator: {comparison_operator}")