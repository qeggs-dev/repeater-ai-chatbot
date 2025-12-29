# ==== 标准库 ==== #
import copy
import aiofiles
from typing import (
    Any,
    Awaitable,
)
import time
from pathlib import Path
import orjson

# ==== 第三方库 ==== #
from loguru import logger

# ==== 自定义库 ==== #
from ..Data_Manager import (
    PromptManager,
    ContextManager
)
from ..User_Config_Manager import (
    ConfigManager,
    UserConfigs
)
from ._objects import (
    ContextObject,
    ContentUnit,
    ContentRole,
    TextBlock,
    ImageBlock,
    ImageUrlBlock,
)
from ._exceptions import *
from TextProcessors import (
    PromptVP,
    limit_blank_lines,
)
from PathProcessors import validate_path, sanitize_filename
from ..Global_Config_Manager import ConfigManager as GlobalConfigManager

# ==== 本模块代码 ==== #
class ContextLoader:
    def __init__(
            self,
            context: ContextManager,
            prompt: PromptManager,
            config: ConfigManager,
        ):
        self._context_manager: ContextManager = context
        self._prompt_manager: PromptManager = prompt
        self._config_manager: ConfigManager = config
    
    async def _load_prompt(
            self,
            context:ContextObject,
            user_id: str,
            temporary_prompt: str | None = None,
            prompt_vp: PromptVP | None = None
        ) -> ContextObject:
        
        user_prompt:str = await self._prompt_manager.load(user_id=user_id, default="")

        if temporary_prompt is not None:
            prompt = temporary_prompt
            logger.info(f"Load Temporary Prompt", user_id = user_id)
        elif user_prompt:
            # 使用用户提示词
            prompt = user_prompt
            logger.info(f"Load User Prompt", user_id = user_id)
        else:
            # 加载默认提示词
            default_prompt_dir = Path(GlobalConfigManager.get_configs().prompt.dir)
            if default_prompt_dir.exists():
                # 如果存在默认提示词文件，则加载默认提示词文件
                config = await self._config_manager.load(user_id)
                
                # 获取默认提示词文件名
                parset_prompt_name = config.parset_prompt_name or GlobalConfigManager.get_configs().prompt.preset_name
                parset_prompt_encoding = GlobalConfigManager.get_configs().prompt.encoding
                suffix = GlobalConfigManager.get_configs().prompt.suffix

                # 加载默认提示词文件
                default_prompt_file = default_prompt_dir / f"{sanitize_filename(parset_prompt_name)}{suffix}"
                if not validate_path(default_prompt_dir, default_prompt_file):
                    raise InvalidPromptPathError(f"Invalid Prompt Path: {default_prompt_file}")
                if default_prompt_file.exists():
                    logger.info(f"Load Default Prompt File: {default_prompt_file}", user_id = user_id)
                    async with aiofiles.open(default_prompt_file, mode="r", encoding=parset_prompt_encoding) as f:
                        prompt = await f.read()
                else:
                    logger.warning(f"Default Prompt File Not Found: {default_prompt_file}", user_id = user_id)
                    prompt = ""
            else:
                logger.warning(f"Default Prompt Directory Not Found: {default_prompt_dir}", user_id = user_id)
                prompt = ""
        
        # 展开变量
        if prompt_vp is not None:
            prompt = await self._expand_variables(prompt, variables_parser = prompt_vp, user_id=user_id)
        logger.debug("Prompt Content:\n{prompt}", user_id = user_id, prompt = prompt)

        # 创建Content单元
        prompt = ContentUnit(
            role = ContentRole.SYSTEM,
            content = prompt
        )
        # 将Content单元加入Context
        context.prompt = prompt
        return context
    
    async def get_context_object(
            self,
            user_id: str
        ) -> ContextObject:
        try:
            context_data = await self._context_manager.load(user_id=user_id, default=[])
        except orjson.JSONDecodeError:
            raise ContextLoadingSyntaxError(f"Context File Syntax Error: {user_id}")
        # 构建上下文对象
        contextObj = ContextObject.from_context(context_data)

        logger.info(f"Load Context: {len(contextObj.context_list)}", user_id = user_id)
        return contextObj

    async def _append_context(
            self,
            context:ContextObject,
            user_id: str,
            new_message: str,
            role: ContentRole = ContentRole.USER,
            role_name: str | None = None,
            image_url: str | list[str] | None = None,
            continue_completion: bool = False,
            prompt_vp: PromptVP | None = None
        ) -> ContextObject:
        """
        添加上下文

        :param context: 上下文对象
        :param user_id: 用户ID
        :param New_Message: 新消息
        :param role: 角色
        :param roleName: 角色名称
        :param continue_completion: 是否继续生成
        :return: 上下文对象
        """
            # 构建上下文对象
        contextObj = await self.get_context_object(user_id=user_id)
        
        if not continue_completion:
            content = ContentUnit()
            if prompt_vp is not None:
                new_message = await self._expand_variables(new_message, variables_parser = prompt_vp, user_id=user_id)
            if image_url:
                if isinstance(image_url, str):
                    content.content = []
                    content.content.append(
                        TextBlock(
                            text = new_message,
                        )
                    )
                    content.content.append(
                        ImageBlock(
                            image_url = ImageUrlBlock(
                                url = image_url,
                            )
                        )
                    )
                elif isinstance(image_url, list):
                    content.content = []
                    content.content.append(
                        TextBlock(
                            text = new_message,
                        )
                    )
                    for url in image_url:
                        content.content.append(
                            ImageBlock(
                                image_url = ImageUrlBlock(
                                    url = url,
                                )
                            )
                        )
                else:
                    raise TypeError(
                        "Invalid content type, must be one of the following: str, list[str], list[ImageUrlBlock]"
                    )
            else:
                content.content = new_message
            content.role = role
            content.role_name = role_name

            # 添加上下文
            if not context.context_list:
                context.context_list = []
            context.context_list += contextObj.context_list
            context.context_list.append(content)
        return context
    
    async def load(
            self,
            user_id: str,
            message: str,
            role: ContentRole = ContentRole.USER,
            role_name: str | None = None,
            temporary_prompt: str | None = None,
            image_url: str | list[str] | None = None,
            load_prompt: bool = True,
            continue_completion: bool = False,
            prompt_vp: PromptVP | None = None,
        ) -> ContextObject:
        """
        加载上下文

        :param user_id: 用户ID
        :param message: 消息内容
        :param role: 角色
        :param role_name: 角色名称
        :param temporary_prompt: 临时提示词
        :param load_prompt: 是否加载提示词
        :param continue_completion: 是否继续生成
        """
        # 如果允许添加提示词，就加载提示词，否则使用空上下文对象
        if load_prompt:
            context = await self._load_prompt(
                ContextObject(),
                user_id=user_id,
                prompt_vp = prompt_vp,
                temporary_prompt = temporary_prompt
            )
        else:
            context = ContextObject()
        
        # 添加上下文
        context = await self._append_context(
            context = context,
            user_id = user_id,
            new_message = message,
            role = role,
            role_name = role_name,
            image_url = image_url,
            continue_completion = continue_completion,
            prompt_vp = prompt_vp
        )
        return context
    
    async def _expand_variables(self, prompt: str, variables_parser: PromptVP, user_id: str) -> str:
        """
        展开变量

        :param prompt: 提示词
        :param variables: 变量
        :param user_id: 用户ID
        """
        variables_parser.reset_counter()
        prompt = variables_parser.process(prompt)
        logger.info(f"Prompt Hits Variable: {variables_parser.hit_var()}/{variables_parser.discover_var()}({variables_parser.hit_var() / variables_parser.discover_var() if variables_parser.discover_var() != 0 else 0:.2%})", user_id = user_id)
        variables_parser.reset_counter()
        prompt = limit_blank_lines(prompt)
        return prompt

    async def save(
            self,
            user_id: str,
            context: ContextObject,
            reduce_to_text:bool = False
        ) -> None:
        """
        保存上下文

        :param user_id: 用户ID
        :param context: 上下文对象
        """
        await self._context_manager.save(user_id, context.to_context(reduce_to_text = reduce_to_text))
        logger.info(f"Save Context: {len(context)}", user_id = user_id)