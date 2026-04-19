from ._client_info import ClientInfo
from openai import AsyncOpenAI
from loguru import logger

class ClientPool:
    def __init__(self):
        self._client_info: dict[ClientInfo, AsyncOpenAI] = {}
    
    def get_client(self, client_info: ClientInfo):
        if client_info in self._client_info:
            logger.info("Using cached client.")
            return self._client_info[client_info]
        else:
            logger.info("Creating new client.")
            client = client_info.to_openai_client()
            self._client_info[client_info] = client
            return client