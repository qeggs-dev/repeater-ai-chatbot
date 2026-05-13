from pydantic import BaseModel, ConfigDict

class ServerConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    host: str | None = None
    port: int | None = None
    workers: int | None = None
    reload: bool | None = None
    restart: bool = False
    run_server: bool = True