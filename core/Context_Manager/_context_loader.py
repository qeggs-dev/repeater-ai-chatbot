# ==== 标准库 ==== #
import asyncio
import orjson
from typing import Any

# ==== 第三方库 ==== #
from loguru import logger
from yarl import URL
from httpx import HTTPStatusError

# ==== 自定义库 ==== #
from ..Assist_Struct import (
    AdditionalData
)
from ..Data_Manager import (
    PromptManager,
    ContextManager
)
from ..User_Config_Manager import (
    ConfigManager
)
from ._objects import (
    ContextObject,
    ContentUnit,
    ContentRole,
    TextBlock,
    ImageBlock,
    ImageUrlBlock,
    VideoBlock,
    VideoUrlBlock,
    AudioBlock,
    AudioDataBlock,
    FileBlock,
    FileDataBlock,
)
from ._exceptions import *
from ..Text_Template_Processer import (
    TemplateParser
)
from PathProcessors import validate_path, sanitize_filename_with_dir
from ..Global_Config_Manager import ConfigManager as GlobalConfigManager
from ..Static_Resources_Client import StaticResourcesClient

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
    
    @property
    @staticmethod
    def empty_content() -> ContentUnit:
        return ContentUnit()
    
    async def load_prompt(
            self,
            user_id: str,
            static_resources_client: StaticResourcesClient,
            temporary_prompt: str | None = None,
            template_parser: TemplateParser | None = None,
        ) -> ContentUnit:
        """
        加载提示词

        :param user_id: 用户ID
        :param temporary_prompt: 临时提示词
        :param prompt_vp: 变量展开处理器
        :return: 提示词
        """
        user_prompt:str = await self._prompt_manager.load(user_id=user_id, default="")
        logger.info("Load Prompt", user_id = user_id)

        if temporary_prompt is not None:
            prompt = temporary_prompt
            logger.info(f"Load Temporary Prompt", user_id = user_id)
        elif user_prompt:
            # 使用用户提示词
            prompt = user_prompt
            logger.info(f"Load User Prompt", user_id = user_id)
        else:
            # 加载默认提示词
            default_prompt_base_path = URL(GlobalConfigManager.get_configs().prompt.base_path)
            # 如果存在默认提示词文件，则加载默认提示词文件
            config = await self._config_manager.load(user_id)
            
            # 获取默认提示词文件名
            parset_prompt_name = config.parset_prompt_name or GlobalConfigManager.get_configs().prompt.preset_name
            parset_prompt_encoding = GlobalConfigManager.get_configs().prompt.encoding
            suffix = GlobalConfigManager.get_configs().prompt.suffix

            # 加载默认提示词文件
            default_prompt_file = default_prompt_base_path / f"{sanitize_filename_with_dir(parset_prompt_name)}{suffix}"
            logger.info(f"Load Default Prompt File: {default_prompt_file}", user_id = user_id)
            try:
                prompt = await static_resources_client.get_text(
                    default_prompt_file,
                    text_encoding = parset_prompt_encoding
                )
            except HTTPStatusError as e:
                logger.error(
                    "Load Default Prompt File Error: {error}",
                    user_id = user_id,
                    error = e.response.text
                )
                prompt = ""
        
        # 展开变量
        if template_parser is not None and prompt:
            prompt = await self._expand_variables(
                user_id = user_id,
                prompt = prompt,
                template_parser = template_parser
            )
        logger.debug("Prompt Content:\n{prompt}", user_id = user_id, prompt = prompt)

        # 创建Content单元
        prompt = ContentUnit(
            role = ContentRole.SYSTEM,
            content = prompt
        )
        return prompt
    
    async def load_context(
            self,
            user_id: str
        ) -> ContextObject:
        """
        加载上下文

        :param user_id: 用户ID
        :return: 上下文对象
        """
        logger.info(
            "Load Context",
            user_id = user_id,
        )
        try:
            context_data = await self._context_manager.load(user_id=user_id, default=[])
        except orjson.JSONDecodeError:
            raise ContextLoadingSyntaxError(f"Context File Syntax Error: {user_id}")
        # 构建上下文对象
        context = ContextObject.from_context(context_data)

        logger.info(f"Load Context: {len(context)}", user_id = user_id)
        return context
    
    async def load(
            self,
            user_id: str,
            static_resources_client: StaticResourcesClient,
            temporary_prompt: str | None = None,
            load_prompt: bool = True,
            template_parser: TemplateParser | None = None,
        ) -> ContextObject:
        """
        加载整个上下文

        :param user_id: 用户ID
        :param temporary_prompt: 临时提示词
        :param load_prompt: 是否加载提示词
        :param template_parser: 模板解析器
        :return: 上下文对象
        """
        # 如果允许添加提示词，就加载提示词，否则使用空上下文对象
        if load_prompt:
            prompt = await self.load_prompt(
                user_id = user_id,
                static_resources_client = static_resources_client,
                template_parser = template_parser,
                temporary_prompt = temporary_prompt
            )
        else:
            prompt = ContextObject()
        
        context = await self.load_context(
            user_id=user_id
        )
        
        context.prompt = prompt
        return context
    
    async def make_user_content(
            self,
            user_id: str,
            new_message: str,
            role: ContentRole = ContentRole.USER,
            role_name: str | None = None,
            enable_user_input_template: bool = False,
            additional_data: AdditionalData | None = None,
            extra_template_fields: dict[str, Any] | None = None,
            template_parser: TemplateParser | None = None
        ) -> ContentUnit:
        """
        Make User Content

        :param user_id: User ID
        :param new_message: User Input Message
        :param role: Content Role
        :param role_name: An optional name for the participant. Provides the model information to differentiate between participants of the same role.
        :param enable_user_input_template: Enable User Input Template Expansion
        :param additional_data: Additional Data
        :param extra_template_fields: Fields to expand in the template
        :param template_parser: Template Parser
        """
        content = ContentUnit()
        if template_parser is not None:
            if enable_user_input_template:
                new_message = await self._expand_variables(
                    user_id = user_id,
                    prompt = new_message,
                    template_parser = template_parser,
                    extra_template_fields = extra_template_fields
                )
        if additional_data is not None:
            if not isinstance(content.content, list):
                content.content = []
            if additional_data.image_url is not None:
                if isinstance(additional_data.image_url, str):
                    content.content.append(
                        TextBlock(
                            text = new_message,
                        )
                    )
                    content.content.append(
                        ImageBlock(
                            image_url = ImageUrlBlock(
                                url = additional_data.image_url,
                            )
                        )
                    )
                elif isinstance(additional_data.image_url, list):
                    for url in additional_data.image_url:
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
            if additional_data.video_url:
                if isinstance(additional_data.video_url, str):
                    content.content.append(
                        VideoBlock(
                            video_url = VideoUrlBlock(
                                url = additional_data.video_url,
                            )
                        )
                    )
                elif isinstance(additional_data.video_url, list):
                    for url in additional_data.video_url:
                        content.content.append(
                            VideoBlock(
                                video_url = VideoUrlBlock(
                                    url = url,
                                )
                            )
                        ) 
                else:
                    raise TypeError(
                        "Invalid content type, must be one of the following: str, list[str], list[VideoUrlBlock]"
                    )
            if additional_data.audio_url:
                if isinstance(additional_data.audio_url, str):
                    content.content.append(
                        AudioBlock(
                            audio_url = AudioDataBlock(
                                data = additional_data.audio_url,
                            )
                        )
                    )
                elif isinstance(additional_data.audio_url, list):
                    for url in additional_data.audio_url:
                        content.content.append(
                            AudioBlock(
                                audio_url = AudioDataBlock(
                                    data = url,
                                )
                            )
                        )
                else:
                    raise TypeError(
                        "Invalid content type, must be one of the following: str, list[str], list[VideoUrlBlock]"
                    )
            if additional_data.file_url:
                if isinstance(additional_data.file_url, str):
                    content.content.append(
                        FileBlock(
                            file_url = FileDataBlock(
                                data = additional_data.file_url,
                            )
                        )
                    )
                elif isinstance(additional_data.file_url, list):
                    for url in additional_data.file_url:
                        content.content.append(
                            FileBlock(
                                file_url = FileDataBlock(
                                    data = url,
                                )
                            )
                        )
                else:
                    raise TypeError(
                        "Invalid content type, must be one of the following: str, list[str]"
                    )
            if new_message:
                content.content.append(
                    TextBlock(
                        text = new_message
                    )
                )
        else:
            content.content = new_message
        content.role = role
        content.role_name = role_name
        return content
    
    async def _expand_variables(
            self,
            user_id: str,
            prompt: str,
            template_parser: TemplateParser,
            extra_template_fields: dict[str, Any] | None = None,
        ) -> str:
        """
        展开变量

        :param prompt: 提示词
        :param user_id: 用户ID
        :param template_parser: 模板解析器
        :param extra_template_fields: 拓展模板字段
        """
        if extra_template_fields is None:
            extra_template_fields = {}
        return await asyncio.to_thread(
            template_parser.render_ex,
            text = prompt,
            user_id = user_id,
            **extra_template_fields
        )

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
        :param reduce_to_text: 是否将上下文对象转换为纯文本
        """
        await self._context_manager.save(user_id, context.to_context(reduce_to_text = reduce_to_text))
        logger.info(f"Save Context: {context.context_item_length}", user_id = user_id)