import ssl

SSL_CONTEXT: ssl.SSLContext = ssl.create_default_context()

def get_ssl_context():
    return SSL_CONTEXT

def set_ssl_context(ssl_context: ssl.SSLContext):
    global SSL_CONTEXT
    SSL_CONTEXT = ssl_context

def update_ssl_context():
    global SSL_CONTEXT
    SSL_CONTEXT = get_ssl_context()