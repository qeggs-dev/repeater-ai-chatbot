from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict
from TextProcessors import text_content_cutter
from .._exceptions import *
from ._content_role import ContentRole
from ._content_block import (
    ContentBlock,
    TextBlock,
    ImageBlock,
    VideoBlock,
    AudioBlock,
    FileBlock
)
from ._function_calling_response import CallingRequest
from typing import Any, Type

class ContentUnit(BaseModel):
    """
    上下文单元
    """
    model_config = ConfigDict(
        validate_assignment = True,
        exclude_none = True
    )

    reasoning_content: str | None = None
    content: str | list[ContentBlock] = ""
    role: ContentRole = ContentRole.USER
    role_name: str |  None = None
    prefix: bool | None = None
    tool_calls: list[CallingRequest] | None = None
    tool_call_id: str | None = None

    def __len__(self) -> int:
        length: int = 0
        if isinstance(self.content, str):
            length = len(self.content)
        else:
            for block in self.content:
                if isinstance(block, TextBlock):
                    length += len(block.text)
        if self.reasoning_content:
            length += len(self.reasoning_content)
        return length
    
    def only_context_block(self, block_type: Type[ContentBlock]) -> None:
        """
        检查上下文单元是否只包含指定类型的ContentBlock
        """
        if isinstance(self.content, str):
            raise ContentUnitError("ContentUnit is not a list of ContentBlock")
        for block in self.content:
            if not isinstance(block, block_type):
                return False
        return True
    
    def remove_context_block(self, block_type: Type[ContentBlock]) -> None:
        """
        移除指定类型的上下文块
        """
        if isinstance(self.content, str):
            raise ContentUnitError("ContentUnit is not a list of ContentBlock")
        new_content: list[ContentBlock] = []
        for block in self.content:
            if not isinstance(block, block_type):
                new_content.append(block)
        self.content = new_content
    
    def to_plaintext_content(self) -> str:
        if isinstance(self.content, str):
            return self.content
        else:
            text_buffer: list[str] = []
            for block in self.content:
                if isinstance(block, TextBlock):
                    text_buffer.append(block.text)
            return "".join(text_buffer)
 
    def to_content(self, remove_reasoning_prompt: bool = False) -> dict[str, Any]:
        if remove_reasoning_prompt:
            return self.model_dump(exclude = {"reasoning_content"})
        return self.model_dump()
    
    def __bool__(self) -> bool:
        return bool(self.content) or bool(self.reasoning_content) or bool(self.tool_call_id)
    
    def reduce_to_text(self):
        if isinstance(self.content, list):
            buffer: list[str] = []
            for block in self.content:
                if isinstance(block, TextBlock):
                    buffer.append(block.text)
            self.content = "\n".join(buffer)
    
    def content_to_string(self, non_text_length_limit: int | None = 10) -> str:
        message_texts: list[str] = []
        for block in self.content:
            if isinstance(block, TextBlock):
                message_texts.append(block.text)
            elif isinstance(block, ImageBlock):
                message_texts.append(
                    f"[Image: {text_content_cutter(block.image_url.url, non_text_length_limit)}]"
                )
            elif isinstance(block, VideoBlock):
                message_texts.append(
                    f"[Video: {text_content_cutter(block.video_url.url, non_text_length_limit)}]"
                )
            elif isinstance(block, AudioBlock):
                message_texts.append(
                    f"[Audio: {text_content_cutter(block.input_audio.data, non_text_length_limit)}]"
                )
            elif isinstance(block, FileBlock):
                message_texts.append(
                    f"[File: {text_content_cutter(block.file.filename, non_text_length_limit)}]"
                )
            else:
                message_texts.append(f"[Unknown Block: {block}]")
    
        return "\n".join(message_texts)

    def __str__(self) -> str:
        text_buffer: list[str] = []
        if self.reasoning_content:
            text_buffer.append("Reasoning:")
            text_buffer.append(self.reasoning_content.replace("\n", "\n  "))
        if self.content:
            text_buffer.append("Content:")
            text_buffer.append(self.content_to_string().replace("\n", "\n  "))
        return "\n".join(text_buffer)