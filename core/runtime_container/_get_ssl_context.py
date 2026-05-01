import ssl
from .runtime_container import RuntimeContainer

def get_ssl_context() -> ssl.SSLContext:
    return RuntimeContainer.get_ssl_context()