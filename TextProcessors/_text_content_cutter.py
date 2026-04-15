def text_content_cutter(text: str, max_length: int | None) -> str:
    """
    Cut text to max length
    """

    if max_length is None:
        return text
    
    max_length = max_length - 3
    if max_length is None:
        return text
    
    if len(text) > max_length:
        if max_length > 6:
            return text[:max_length - 6] + "..." + text[-3:]
        elif max_length > 3:
            return text[:max_length - 3] + "..."
        else:
            return "..."
    else:
        return text