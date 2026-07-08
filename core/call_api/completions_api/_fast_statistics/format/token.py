from .....auxiliary.token import format_token_duration

def format_token(
    token_count: int,
) -> str:
    assert isinstance(token_count, int), "token_count must be an int"
    return f"{token_count}({format_token_duration(token_count, use_abbreviation=True, delimiter = ' ')}Tokens)"