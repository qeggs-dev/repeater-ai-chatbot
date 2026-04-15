from typing import Generator
from ..Request_Log import RequestLog
from ..CallAPI.CompletionsAPI import Request, Response
from ..Context_Manager import ContextObject, ContentUnit
from pydantic import BaseModel, Field

class MultiResponse(BaseModel):
    historical_context: ContextObject = Field(default_factory=ContextObject)
    responses: list[Response] = Field(default_factory=list)
    tool_requests: list[list[ContentUnit]] = Field(default_factory=list)

    def __getitem__(self, key: int | slice) -> Response:
        if isinstance(key, int | slice):
            return self.responses[key]
        else:
            raise TypeError("Invalid key type")

    def add(self, response: Response):
        self.responses.append(response)

    def new_contexts(self):
        context = ContextObject()
        for index, response in enumerate(self.responses):
            context.extend(response.new_context)
            if index < len(self.tool_requests):
                context.extend(self.tool_requests[index])
        return context
    
    def request_logs(self) -> list[RequestLog]:
        return [response.request_log for response in self.responses]
    
    def __iter__(self) -> Generator[Response, None, None]:
        for response in self.responses:
            yield response