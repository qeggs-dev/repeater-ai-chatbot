from httpx import Timeout
from pydantic import BaseModel

class ClientTimeout(BaseModel, frozen=True):
    connect: int | float | None = None
    read: int | float | None = None
    write: int | float | None = None
    pool_connect: int | float | None = None
    
    def to_timeout(self) -> Timeout:
        return Timeout(
            connect = self.connect,
            read = self.read,
            write = self.write,
            pool_connect = self.pool_connect
        )