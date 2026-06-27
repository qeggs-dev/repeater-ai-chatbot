from pydantic import BaseModel, ConfigDict

class StaticConfig(BaseModel):
    readme_file_path: str = "./README.md"
    static_dir: str = "./static"