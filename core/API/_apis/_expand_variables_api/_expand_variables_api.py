import asyncio

from ..._resource import Resource
from fastapi.responses import PlainTextResponse
from ....Text_Template_Processer import TemplateParser
from ....Global_Config_Manager import ConfigManager as Global_Config_Manager
from ....User_Config_Manager import ConfigManager
from ._requests import ExpandVariableRequest
from jinja2 import TemplateError

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
        user_config = config,
    )

    # 调用PromptVP类处理文本
    try:
        output = await asyncio.to_thread(
            template_parser.render_ex,
            request.text,
            user_id = user_id,
        )
        # 返回结果
        return PlainTextResponse(output)
    except TemplateError as e:
        output = f"{e.__class__.__name__}: {e.message}"
        return PlainTextResponse(
            output,
            status_code = 400
        )
    except Exception as e:
        output = f"{e.__class__.__name__}: {str(e)}"
        return PlainTextResponse(
            output,
            status_code = 400
        )