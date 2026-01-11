import warnings

from ..._resource import Resource
from ....Assist_Struct import Request_User_Info
from fastapi.responses import PlainTextResponse
from loguru import logger
from ....Text_Template_Processer import PromptVP_Loader
from ....Global_Config_Manager import ConfigManager as Global_Config_Manager
from ....User_Config_Manager import ConfigManager
from ._requests import ExpandVariableRequest

prompt_vp_loader = PromptVP_Loader()

warnings.showwarning

@Resource.app.post("/variable_expand/{user_id}")
async def expand_variables(user_id: str, request: ExpandVariableRequest):
    """
    Endpoint for expanding variables
    """
    # 初始化加载器
    config_loader = ConfigManager()

    # 获取用户配置
    config = await config_loader.load(user_id=user_id)

    if request.user_info.username is None:
        user_name = user_id
    else:
        user_name = request.user_info.username
    
    # 调用PromptVP类处理文本
    prompt_vp = prompt_vp_loader.get_prompt_vp_ex(
        user_id = user_id,
        user_info = Request_User_Info(
            username = user_name,
            nickname = request.user_info.nickname,
            age = request.user_info.age,
            gender = request.user_info.gender
        ),
        global_config = Global_Config_Manager.get_configs(),
        config = config
    )
    output = prompt_vp.process(request.text)

    # 日志输出命中信息
    logger.info(f"Prompt Hits Variable: {prompt_vp.hit_var()}/{prompt_vp.discover_var()}({prompt_vp.hit_var() / prompt_vp.discover_var() if prompt_vp.discover_var() != 0 else 0:.2%})", user_id = user_id)

    # 返回结果
    return PlainTextResponse(output)