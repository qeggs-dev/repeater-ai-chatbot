from pydantic import BaseModel, ConfigDict

class StaticConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    readme_file_path: str = "./README.md"
    static_dir: str = "./static"