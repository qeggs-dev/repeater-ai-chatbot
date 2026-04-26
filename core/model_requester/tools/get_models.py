from ...context import ToolCallPacakage, CallType
from ...data_manager import PromptManager
from .._caller import ModelRequester
from ...runtime_container import RuntimeContainer
from ...model_api import ModelType
from pydantic import BaseModel

@ModelRequester.reg_global_package
class GetModels(ToolCallPacakage):
    prompt_manager: PromptManager = PromptManager()
    name = "get_models"
    document = "Gets a list of all available models."
    call_type = CallType.ASYNC

    class Params(BaseModel):
        model_type: ModelType = ModelType.CHAT

    async def call(self, args: Params):
        response = await RuntimeContainer.get_runtime().model_api_manager.get_models(
            args.model_type,
            with_api_key = False
        )
        return response.model_dump()