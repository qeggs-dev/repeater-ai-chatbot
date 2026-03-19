from pydantic import BaseModel, ConfigDict, Field
from ._models import *

class Global_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    blacklist: BacklistConfig = Field(default_factory=BacklistConfig)
    callapi: CallAPIConfig = Field(default_factory=CallAPIConfig)
    context: ContextConfig = Field(default_factory=ContextConfig)
    global_exception_handler: GlobalExceptionHandlerConfig = Field(default_factory=GlobalExceptionHandlerConfig)
    licenses: LicensesConfig = Field(default_factory=LicensesConfig)
    logger: LoggerConfig = Field(default_factory=LoggerConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    model_api: ModelAPIConfig = Field(default_factory=ModelAPIConfig)
    nexus: NexusConfig = Field(default_factory=NexusConfig)
    text_template: TextTemplateConfig = Field(default_factory=TextTemplateConfig)
    prompt: PromptConfig = Field(default_factory=PromptConfig)
    render: RenderConfig = Field(default_factory=RenderConfig)
    request_log: RequestLogConfig = Field(default_factory=RequestLogConfig)
    server: ServerConfig = Field(default_factory=ServerConfig)
    static: StaticConfig = Field(default_factory=StaticConfig)
    static_resources_server: StaticResourcesServerConfig = Field(default_factory=StaticResourcesServerConfig)
    user_config_cache: UserConfigCacheConfig = Field(default_factory=UserConfigCacheConfig)
    user_data: UserDataConfig = Field(default_factory=UserDataConfig)
    user_nickname_mapping: UserNicknameMappingConfig = Field(default_factory=UserNicknameMappingConfig)
    web: WebConfig = Field(default_factory=WebConfig)