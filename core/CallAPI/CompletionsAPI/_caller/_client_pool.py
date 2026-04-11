from ._client_info import ClientInfo
from openai import AsyncOpenAI

class ClientPool:
    def __init__(self):
        self._client_info: dict[ClientInfo, AsyncOpenAI] = {}
    
    def get_client(self, client_info: ClientInfo):
        if client_info in self._client_info:
            return self._client_info[client_info]
        else:
            client = client_info.to_openai_client()
            self._client_info[client_info] = client
            return client