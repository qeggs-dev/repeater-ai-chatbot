from ...context_manager import ToolCallPacakage
from ...data_manager import PromptManager
from .._caller import ModelRequester
from pydantic import BaseModel

@ModelRequester.reg_global_package
class SetPrompt(ToolCallPacakage):
    class Params(BaseModel):
        prompt: str

    prompt_manager: PromptManager = PromptManager()
    name = "set_prompt"

    def document(self):
        return "Overrides the current system prompt."

    def call(self, args: Params):
        self.prompt_manager.save(args.prompt)
        return "Prompt seted."