from pydantic import BaseModel

class RequirementsConfig(BaseModel):
    enable_check: bool = True
    requirements_file: str = "requirements.txt"