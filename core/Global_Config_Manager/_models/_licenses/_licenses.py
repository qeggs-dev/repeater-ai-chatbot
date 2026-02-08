from pydantic import BaseModel, Field

class Licenses_Config(BaseModel):
    license_dir: str = "./LICENSES"
    license_encoding: str = "utf-8"
    self_license_files: dict[str, str] = Field(default_factory=lambda: {"MIT": "./LICENSE"})