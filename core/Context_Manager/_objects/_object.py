from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict, validate_call
from typing import overload, Iterable, Any
from .._exceptions import *
from ._func_calling_objects import CallingFunctionResponse
from ._content_role import ContentRole
from ._content_unit import ContentUnit


class ContextObject(BaseModel):
    """
    上下文对象
    """
    model_config = ConfigDict(
        validate_assignment = True,
        exclude_none = True
    )

    prompt: ContentUnit | None = None
    context_list: list[ContentUnit] = Field(default_factory=list)

    def __bool__(self) -> bool:
        return bool(self.prompt or self.context_list)

    @overload
    def __getitem__(self, index: int) -> ContentUnit:
        ...

    @overload
    def __getitem__(self, index: slice) -> ContextObject:
        ...
    
    def __getitem__(self, index: int | slice):
        """
        获取上下文列表中的指定项
        
        :param index: 索引
        :return: 指定项
        """
        if isinstance(index, int):
            return self.context_list[index]
        elif isinstance(index, slice):
            return ContextObject(
                prompt=self.prompt,
                context_list=self.context_list[index]
            )
        else:
            raise TypeError("index must be int or slice")
    
    def __setitem__(self, index: int | slice, value: ContentUnit | Iterable[ContentUnit]):
        """
        设置上下文列表中的指定项
        
        :param index: 索引
        :param value: 值
        :return: 构建的对象
        """
        self.context_list[index] = value

    def __len__(self):
        """
        获取上下文列表的长度

        :return: 上下文列表的长度
        """
        if self.prompt is not None:
            if len(self.prompt) > 0:
                return len(self.context_list) + 1
        return self.context_item_length
    
    def __iter__(self):
        """
        迭代上下文列表
        
        :return: 上下文列表的迭代器
        """
        # 先 yield 提示词
        if self.prompt:
            yield self.prompt
        # 再正常遍历 context_list
        for content in self.context_list:
            yield content
    
    @validate_call
    def update_from_context(self, context: list[dict]) -> None:
        """
        从上下文列表更新上下文
        
        :param context: 上下文列表
        :return: 构建的对象
        """
        other = self.from_context(context)
        self.context_list = other.context_list
        self.prompt = other.prompt
    
    @validate_call
    def rewrite(self, content: ContentUnit, index: int = -1) -> None:
        """
        重写上下文列表中的指定项

        :param content: 内容
        :return: 构建的对象
        """
        if not isinstance(content, ContentUnit):
            raise TypeError("content must be a ContentUnit object")
        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        if abs(index) > len(self.context_list):
            raise IndexError("index out of range")
        
        self.context_list[index] = content
    
    @property
    def context_item_length(self):
        """
        获取上下文列表的长度
        
        :return: 上下文列表的长度
        """
        if self.prompt:
            return len(self.context_list) + 1
        return len(self.context_list)

    @property
    def total_length(self) -> int:
        """
        获取上下文总长度
        
        :return: 上下文总长度
        """
        return (
            sum([len(content) for content in self.context_list])
            +
            (len(self.prompt) if self.prompt else 0)
        )
    
    @property
    def average_length(self) -> float:
        """
        获取上下文平均长度

        :return: 上下文平均长度
        """
        if len(self) == 0:
            return 0
        return self.total_length / len(self)

    @validate_call
    def to_context(self, remove_resoning_prompt: bool = False, reduce_to_text: bool = False) -> list[dict]:
        """
        获取上下文

        :param remove_reasoner_prompt: 是否移除reasoner提示词
        :param reduce_to_text: 是否将上下文内容退化为纯文本
        """
        context_list = []
        if self.context_list:
            for content in self.context_list:
                if reduce_to_text:
                    content.reduce_to_text()
                context_list.append(content.to_content(remove_resoning_prompt))
        return context_list
    
    @property
    def context(self) -> list[dict]:
        """
        获取上下文
        """
        return self.to_context(False, False)
    
    @validate_call
    def to_full_context(self, remove_resoning_prompt: bool = False, reduce_to_text: bool = False) -> list[dict]:
        """
        获取上下文，如果有提示词，则添加到最前面

        :param remove_reasoner_prompt: 是否移除reasoner提示词
        :param reduce_to_text: 是否将上下文内容退化为纯文本
        """
        context_list: list[dict[str, Any]] = []
        if self.prompt:
            if reduce_to_text:
                self.prompt.reduce_to_text()
            context_list.append(self.prompt.to_content(remove_resoning_prompt))
        context_list.extend(self.to_context(remove_resoning_prompt, reduce_to_text))
        return context_list
    
    @property
    def full_context(self) -> list[dict]:
        """
        获取上下文，如果有提示词，则添加到最前面
        """
        return self.to_full_context(False, False)
    
    @validate_call
    def withdraw(self, length: int | None = None):
        """
        撤销指定长度的内容

        :param length: 撤销长度
        :return: 撤销的内容
        """
        if length is None:
            pop_items: list[ContentUnit] = []
            
            # 安全检查
            if not self.context_list:
                return ContextObject()
            try:
                # 第一步：pop直到找到助手消息
                while (self.context_list and 
                    self.last_content.role != ContentRole.ASSISTANT):
                    pop_items.append(self.context_list.pop())
                
                # 第二步：pop助手消息
                while (self.context_list and 
                    self.last_content.role == ContentRole.ASSISTANT):
                    pop_items.append(self.context_list.pop())
                
                # 第三步：pop相关联的用户消息
                while (self.context_list and 
                    self.last_content.role != ContentRole.ASSISTANT):
                    pop_items.append(self.context_list.pop())
            except IndexError:
                pass
            
            return ContextObject(
                prompt = None,
                context_list = pop_items[::-1],
            )
        elif isinstance(length, int):
            if length > len(self.context_list):
                raise ValueError("length is too long")
            if length <= 0:
                raise ValueError("length is too short")
            
            # 检查索引是否在上下文范围内
            if 0 <= length < len(self.context_list):
                return self.pop_last_n(length)
            else:
                raise IndexError("Index out of range")
        else:
            raise TypeError("length must be int or None")
    
    @validate_call
    def insert(self, content_unit: ContentUnit, index: int | None = None):
        """
        插入内容单元到上下文列表中

        :param content_unit: 内容单元
        :param index: 插入位置，默认为None，表示插入到末尾
        """
        if index is None:
            self.context_list.append(content_unit)
        elif abs(index) <= len(self.context_list):
            raise IndexError("Index out of range")
        else:
            self.context_list.insert(index, content_unit)
        return self
    
    @property
    def last_content(self) -> ContentUnit:
        """
        获取最后一个上下文单元
        """
        if not self.context_list:
            self.context_list.append(ContentUnit())
        return self.context_list[-1]
    
    @validate_call
    def append(self, content: ContentUnit) -> None:
        """
        添加上下文单元
        """
        self.context_list.append(content)
    
    def extend(self, content: ContextObject | list[ContentUnit]) -> None:
        """
        扩展上下文单元
        """
        if isinstance(content, ContextObject):
            self.context_list.extend(content.context_list)
        elif isinstance(content, list):
            self.context_list.extend(content)
        else:
            raise TypeError("content must be a list of ContentUnit or ContextObject")
    
    def append_content(
        self,
        reasoning_content:str = "",
        content: str = "",
        role: ContentRole = ContentRole.USER,
        role_name: str |  None = None,
        is_prefix: bool | None = None,
        tool_call_id: str = "",
    ):
        """
        添加上下文内容

        :param reasoning_content: Resoning 内容
        :param content: 内容
        :param role: 角色
        :param role_name: 角色名称
        :param is_prefix: 是否为前缀(用于提交给模型用于续写)
        :param funcResponse: 函数响应
        :param tool_call_id: 工具调用ID
        """
        self.append(
            ContentUnit(
                reasoning_content = reasoning_content,
                content = content,
                role = role,
                role_name = role_name,
                prefix = is_prefix,
                tool_call_id = tool_call_id,
            )
        )
    
    @validate_call
    def pop(self, index: int = -1) -> ContentUnit:
        """
        弹出一个上下文单元

        :param index: 弹出第几个上下文单元，默认为最后一个
        :return: 弹出的上下文单元
        :raises IndexOutOfRangeError: 如果index超出范围，则抛出该异常
        """
        if abs(index) > len(self.context_list):
            raise IndexOutOfRangeError("index out of range")
        
        return self.context_list.pop(index)
    
    @validate_call
    def pop_last_n(self, n: int) -> list[ContentUnit]:
        """
        弹出最后n个上下文单元

        :param n: 弹出的元素个数
        :return: 弹出的元素列表
        :raises IndexOutOfRangeError: 数量超出范围
        """
        if n > len(self.context_list) or n < 0:
            raise IndexOutOfRangeError("index out of range")
        
        pop_list:list[ContentUnit] = self.context_list[-n:]
        self.context_list = self.context_list[:-n]
        return pop_list
    
    @validate_call
    def pop_begin_n(self, n: int) -> list[ContentUnit]:
        """
        弹出头部的n个元素

        :param n: 弹出的元素个数
        :return: 弹出的元素列表
        :raise IndexOutOfRangeError: 数量超出范围
        """
        if n > len(self.context_list) or n < 0:
            raise IndexOutOfRangeError("index out of range")
        
        pop_list = self.context_list[:n]
        self.context_list = self.context_list[n:]
        return pop_list
    
    @property
    def is_empty(self) -> bool:
        """
        判断上下文是否为空
        """
        return not self.prompt and not self.context_list
    
    @property
    def has_new_func_calling_response(self) -> bool:
        """
        判断上下文是否包含新的函数调用响应
        """
        return self.last_content.funcResponse is not None
    
    @validate_call
    def shrink(self, length: int, ensure_role_at_top: ContentRole = ContentRole.USER):
        """
        缩小上下文长度
        
        :param length: 上下文总字数
        :param ensure_role_at_top: 确保指定角色在顶部
        :raise IndexOutOfRangeError: 数量超出范围
        """
        if not isinstance(length, int):
            raise TypeError("length must be int")
        if not isinstance(ensure_role_at_top, ContentRole):
            raise TypeError("ensure_role_at_top must be ContentRole")

        if length < 0:
            raise IndexOutOfRangeError("length must be positive")

        # 当length大于等于实际长度时，不做任何事
        if abs(length) >= self.total_length:
            return
        
        while self.total_length > length:
            self.pop_begin_n(1)
        
        if self.context_list and self.context_list[0].role != ensure_role_at_top:
            # 从头部寻找第一个为ensure_role_at_top的ContextUnit
            for i in range(len(self.context_list)):
                if self.context_list[i].role == ensure_role_at_top:
                    self.context_list = self.context_list[i:]
                    break
            else:
                raise IndexOutOfRangeError(f"Role {ensure_role_at_top} not found in context_list")
    
    def copy(self) -> ContextObject:
        """
        复制对象
        :return: 复制后的对象
        """
        return ContextObject(
            prompt = self.prompt,
            context_list = self.context_list.copy(),
        )
    
    @classmethod
    def from_context(cls, context: list[dict[str, Any]]) -> ContextObject:
        """
        从上下文列表构建对象
        
        :param context: 上下文列表
        :return: 构建的对象
        """
        if not isinstance(context, list):
            raise TypeError("context must be list")
        contextObj = cls()
        contextObj.context_list = []
        for content in context:
            if not isinstance(content, dict):
                raise TypeError("context must be list of dict")
            contextObj.context_list.append(ContentUnit(**content))
        return contextObj
        