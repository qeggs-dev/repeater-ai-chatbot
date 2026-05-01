from ._client_info import ClientInfo
from httpx import AsyncClient
from loguru import logger

class ClientPool:
    def __init__(self):
        self._clients: dict[ClientInfo, AsyncClient] = {}
        self._cache_hits: int = 0
        self._cache_misses: int = 0
    
    def get_client(self, client_info: ClientInfo):
        if client_info in self._clients:
            client = self._clients[client_info]
            self._cache_hits += 1
            logger.info(
                "Using cached client. (Cache hit rate: {cache_hit_rate:.2%})",
                cache_hit_rate = self._cache_hits / (self._cache_hits + self._cache_misses)
            )
            return client
        else:
            client = client_info.to_client()
            self._clients[client_info] = client
            self._cache_misses += 1
            logger.info(
                "Creating new client. (Cache hit rate: {cache_hit_rate:.2%})",
                cache_hit_rate = self._cache_hits / (self._cache_hits + self._cache_misses)
            )
            return client
    
    def remove_client(self, client_info: ClientInfo):
        if client_info in self._clients:
            self._clients.pop(client_info)
        else:
            logger.warning(
                "Client not found in pool.",
            )
    
    def reset_cache_stats(self):
        self._cache_hits = 0
        self._cache_misses = 0
    
    def clear(self):
        self._clients.clear()