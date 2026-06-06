from pydantic import BaseModel, Field
from ...context import ToolCallPacakage, CallType
from ...data_manager import PromptManager
from .._caller import ModelRequester
from ...runtime_container import RuntimeContainer
from ...clients.model_info import ModelAPIResponse, SafeModelInfo

@ModelRequester.reg_global_package
class GetModels(ToolCallPacakage):
    prompt_manager: PromptManager = PromptManager()
    name = "get_models"
    document = "Gets a list of all available models."
    call_type = CallType.ASYNC

    class Params(BaseModel):
        model_id: str | None = Field(None, description = "Model query expression.")
        detailed_info: bool = Field(False, description = "More detailed model information.")
    
    class Result(BaseModel):
        models: list[SafeModelInfo] = Field(default_factory=list)

    async def call(self, args: Params):
        runtime = RuntimeContainer.get_runtime()
        if args.model_id is None:
            response = await runtime.model_info_client.get_all_models()
        else:
            response = await runtime.model_info_client.get_models(model_id = args.model_id)
        
        if response.code == 200:
            model_info = response.get_data()
            if model_info is None:
                raise ValueError("Model info is None")
            return self.Result(
                models = [model.to_safe(args.detailed_info) for model in model_info.models]
            ).model_dump(exclude_none = True)
        else:
            raise ValueError(f"Failed to get models: {response.text}")