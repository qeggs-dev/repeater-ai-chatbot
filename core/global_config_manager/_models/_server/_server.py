from pydantic import BaseModel, ConfigDict

class ServerConfig(BaseModel):
    host: str | None = None
    port: int | None = None
    workers: int | None = None
    reload: bool | None = None
    restart: bool = False
    run_server: bool = True