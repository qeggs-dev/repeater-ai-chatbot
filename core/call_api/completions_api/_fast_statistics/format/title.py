def format_title(
    title: str,
    dividing: str = "=",
    title_width: int = 50
):
    assert isinstance(title, str), "title must be a str"
    assert isinstance(dividing, str), "dividing must be a str"
    assert isinstance(title_width, int), "title_width must be an int"
    return f" {title} ".center(title_width, dividing)