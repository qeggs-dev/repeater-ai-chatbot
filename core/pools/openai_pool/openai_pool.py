from ..client_pool import ClientInfo, ClientPool
from openai import AsyncOpenAI

class OpenAIPool:
    def __init__(self, cache_size: int | float = 1000):
        self._clients = ClientPool(
            cache_size = cache_size
        )
    
    def get_openai(self, client_info: ClientInfo, api_key: str):
        client = self._clients.get_client(client_info)
        openai = AsyncOpenAI(
            api_key = api_key,
            base_url = client_info.url,
            timeout = client_info.timeout,
            http_client = client,
        )
        return openai
    
    def reset_cache_stats(self):
        self._clients.reset_cache_stats()
    
    def clear(self):
        self._clients.clear()