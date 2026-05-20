from pythonping import payload_provider
from typing import Union

PayloadProvider = Union[
    payload_provider.PayloadProvider,
    payload_provider.List,
    payload_provider.Repeat,
    payload_provider.Sweep
]