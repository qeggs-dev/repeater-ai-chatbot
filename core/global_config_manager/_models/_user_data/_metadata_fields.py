from pydantic import BaseModel

class MetadataFields(BaseModel):
    """
    Metadata Fields
    """
    branch_field: str = "default_branch"