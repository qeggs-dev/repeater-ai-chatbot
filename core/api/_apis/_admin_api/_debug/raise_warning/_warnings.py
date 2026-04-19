# https://docs.python.org/3.11/library/exceptions.html

WARNINGS: dict[str, type[Warning]] = {
    "Warning": Warning,
    "UserWarning": UserWarning,
    "DeprecationWarning": DeprecationWarning,
    "PendingDeprecationWarning": PendingDeprecationWarning,
    "SyntaxWarning": SyntaxWarning,
    "RuntimeWarning": RuntimeWarning,
    "FutureWarning": FutureWarning,
    "ImportWarning": ImportWarning,
    "UnicodeWarning": UnicodeWarning,
    "EncodingWarning": EncodingWarning,
    "BytesWarning": BytesWarning,
    "ResourceWarning": ResourceWarning,
}