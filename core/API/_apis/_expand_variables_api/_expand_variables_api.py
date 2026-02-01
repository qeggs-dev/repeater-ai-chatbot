from ..._resource import Resource
from fastapi.responses import PlainTextResponse
from ....Text_Template_Processer import TemplateParser
from ....Global_Config_Manager import ConfigManager as Global_Config_Manager
from ....User_Config_Manager import ConfigManager
from ._requests import ExpandVariableRequest

@Resource.app.post("/variable_expand/{user_id}")
async def expand_variables(user_id: str, request: ExpandVariableRequest):
    """
    Endpoint for expanding variables
    """
    # 初始化加载器
    config_loader = ConfigManager()

    # 获取用户配置
    config = await config_loader.load(user_id=user_id)

    template_parser = TemplateParser(
        user_info = request.user_info,
        global_config = Global_Config_Manager.get_configs(),
        config = config,
    )

    # 调用PromptVP类处理文本
    output = template_parser.render_ex(
        request.text,
        user_id = user_id,
    )

    # 返回结果
    return PlainTextResponse(output)