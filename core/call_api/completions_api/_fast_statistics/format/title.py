def format_title(
    title: str,
    dividing: str = "=",
    title_width: int = 50
):
    return f" {title} ".center(title_width, dividing)