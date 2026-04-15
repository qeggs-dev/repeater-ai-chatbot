from pydantic import BaseModel
from ....Context_Manager import CallingRequest, SpecifiedFunction

class ToolCall(BaseModel):
    """
    Dataclass to store the delta data for a given date.
    """
    id: str = ""
    type: str = ""
    name: str = ""
    arguments: str = ""

    def to_calling_request(self) -> CallingRequest:
        return CallingRequest(
            id = self.id,
            type = self.type,
            function = SpecifiedFunction(
                name = self.name,
                arguments = self.arguments
            )
        )