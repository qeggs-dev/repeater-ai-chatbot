from pydantic import BaseModel

class StaticResourcesServerConfig(BaseModel):
    """Static resources server model"""
    base_url: str | None = None
    timeout: int | float | None = None