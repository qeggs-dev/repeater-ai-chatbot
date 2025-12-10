def format_carry_duration(
    value: int,
    levels: list[tuple[str, str, int]],
    start_with: int = 0,
    use_abbreviation: bool = False,
    delimiter: str = ", ",
    final_level: tuple[str, str] = ("max_level", "max"),
    negative_prompt: str = "(Negative) "
) -> str:
    """
    Format a value using a carry system with specified levels.

    Args:
        value (int): The value to format.
        levels (list[tuple[str, str, int]]): List of (name, abbreviation, divisor) tuples.
        start_with (int, optional): The starting index in levels. Defaults to 0.
        use_abbreviation (bool, optional): Whether to use abbreviations. Defaults to False.
        delimiter (str, optional): Delimiter between units. Defaults to ", ".
        final_level (tuple[str, str], optional): Final level (name, abbreviation). Defaults to ("max_level", "max").

    Returns:
        str: Formatted value string.
    """
    if not levels:
        raise ValueError("levels cannot be empty")
    
    if start_with not in range(len(levels)):
        raise ValueError(f"start_with must be in range [0, {len(levels)})")
    
    # Handle zero value
    if value == 0:
        name, abbr = levels[0][:2] if levels else ("unit", "unit")
        return f"0 {abbr if use_abbreviation else name}"
    
    # Handle negative value
    is_negative = value < 0
    value = abs(value)
    
    end_level, end_level_abbreviation = final_level
    data_level_stack: list[str] = []
    remaining_part: int = value
    
    # Process each level starting from the specified level
    for name, abbreviation, divisor in levels[start_with:]:
        if remaining_part == 0:
            break
            
        current_value = remaining_part % divisor
        remaining_part //= divisor
        
        if current_value > 0:
            unit = abbreviation if use_abbreviation else name
            # Handle pluralization
            if current_value != 1 and not use_abbreviation:
                unit += "s"
            data_level_stack.append(f"{current_value} {unit}")
        
        if remaining_part == 0:
            break
    
    # Handle the final level
    if remaining_part > 0:
        unit = end_level_abbreviation if use_abbreviation else end_level
        if remaining_part != 1 and not use_abbreviation:
            unit += "s"
        data_level_stack.append(f"{remaining_part} {unit}")
    
    # Reverse the stack to get the correct order (largest to smallest)
    text = delimiter.join(data_level_stack[::-1])
    
    if is_negative:
        text = f"{negative_prompt}{text}"
    
    return text

# Example usage with custom levels
def example():
    # Custom example 1: Bytes formatting
    BYTE_LEVELS = [
        ("byte", "B", 1024),
        ("kilobyte", "KB", 1024),
        ("megabyte", "MB", 1024),
        ("gigabyte", "GB", 1024),
        ("terabyte", "TB", 1024),
    ]
    
    print("\nBytes formatting:")
    print(format_carry_duration(
        1234567890123,
        levels=BYTE_LEVELS,
        final_level=("petabyte", "PB")
    ))
    
    # Custom example 2: Metric prefixes
    METRIC_LEVELS = [
        ("unit", "u", 1000),
        ("thousand", "K", 1000),
        ("million", "M", 1000),
        ("billion", "B", 1000),
    ]
    
    print("\nMetric formatting:")
    print(format_carry_duration(
        123456789,
        levels=METRIC_LEVELS,
        final_level=("trillion", "T"),
        use_abbreviation=True
    ))
    
    # Custom example 3: Custom time units
    SIMPLE_TIME_LEVELS = [
        ("second", "s", 60),
        ("minute", "m", 60),
        ("hour", "h", 24),
        ("day", "d", 7),
    ]
    
    print("\nSimple time formatting:")
    print(format_carry_duration(
        1234567,
        levels=SIMPLE_TIME_LEVELS,
        final_level=("week", "w"),
        use_abbreviation=True
    ))


if __name__ == "__main__":
    example()