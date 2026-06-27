from pydantic import BaseModel

class StaticResourcesServerConfig(BaseModel):
    """Static resources server model"""
    base_url: str = ""
    timeout: int | float | None = None