import ssl

class SSLContext:
    def __init__(self):
        self.ssl_context: ssl.SSLContext = ssl.create_default_context()

    def get_ssl_context(self):
        return self.ssl_context
    
    def set_ssl_context(self, ssl_context: ssl.SSLContext):
        self.ssl_context = ssl_context

    def update_ssl_context(self):
        self.ssl_context = ssl.create_default_context()

ssl_context = SSLContext()

def get_ssl_context():
    global ssl_context
    return ssl_context.get_ssl_context()

def set_ssl_context(new_ssl_context: ssl.SSLContext):
    global ssl_context
    ssl_context.set_ssl_context(new_ssl_context)

def update_ssl_context():
    global ssl_context
    ssl_context.update_ssl_context()