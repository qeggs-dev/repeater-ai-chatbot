# ==== 标准库 ==== #
import time
import asyncio
from abc import ABC, abstractmethod

# ==== 第三方库 ==== #
from loguru import logger

# ==== 自定义库 ==== #
from .._objects import (
    Request,
    Response,
    Runtime
)
from ....pools.awaitable_pool import CoroutinePool
from .._caller import (
    CallAPI,
    StreamAPI
)
from .._fast_statistics import FastStatistics

class ClientBase(ABC):
    def __init__(self, max_concurrency: int = 1000):
        # 协程池
        self.coroutine_pool = CoroutinePool(max_concurrency)
    # region 协程池管理
    async def set_concurrency(self, new_max: int = 1000):
        """动态修改并发限制"""
        await self.coroutine_pool.set_concurrency(new_max)
    # endregion

    # region 提交任务
    @abstractmethod
    async def submit_request(self, user_id:str, request: Request, runtime: Runtime) -> Response:
        """提交请求，并等待API返回结果"""
        pass
    # endregion

    # region 预处理响应数据
    async def _preprocess_response(self, user_id: str, request: Request, response: Response, runtime: Runtime):
        assert isinstance(user_id, str)
        assert isinstance(request, Request)
        assert isinstance(response, Response)

        with runtime.status_stack.enter("Logging Response Content"):
            last_content = response.new_context.last_content
            if last_content is not None:
                if last_content.reasoning_content:
                    logger.info(
                        "Reasoning_Content: \n\n{reasoning_content}\n",
                        reasoning_content = last_content.reasoning_content,
                        user_id = user_id,
                        donot_send_console = True
                    )
                if last_content.content:
                    logger.info(
                        "Content: \n\n{content}\n",
                        content = last_content.content,
                        user_id = user_id,
                        donot_send_console = True
                    )
        
        with runtime.status_stack.enter("Fast Statistics"):
            await asyncio.to_thread(
                self._print_fast_statistics,
                user_id = user_id,
                request = request,
                response = response
            )
        return response
    # endregion

    # region 任务
    async def _submit_task(self, user_id: str, request: Request, runtime: Runtime):
        assert isinstance(user_id, str), "user_id must be a string"
        assert isinstance(request, Request), "request must be a Request object"
        assert isinstance(runtime, Runtime), "runtime must be a Runtime object"

        if request.stream:
            client = StreamAPI()
        else:
            client = CallAPI()
        return await client.call(
            user_id = user_id,
            request = request,
            runtime = runtime
        ), client
    # endregion

    # region 打印日志
    def _print_fast_statistics(self, user_id: str, request: Request, response: Response):
        """
        快速统计请求内容并输出到日志中

        :param user_id: 用户ID
        :param request: 请求对象
        :param response: 响应对象
        """
        assert isinstance(user_id, str), "user_id must be a string"
        assert isinstance(request, Request), "request must be a Request object"
        assert isinstance(response, Response), "response must be a Response object"

        fs_logger = logger.bind(user_id = user_id)

        fs_logger.info("Generating fast statistics...")

        buffer: list[str] = []

        fast_statistics_start_time = time.perf_counter_ns()
        fast_statistics = FastStatistics(
            user_id = user_id,
            request = request,
            response = response,
        )
        fast_statistics_end_time = time.perf_counter_ns()

        format_start_time = time.perf_counter_ns()
        buffer.extend(
            fast_statistics.format_statistics_stream(
                title_width = 50
            )
        )
        format_end_time = time.perf_counter_ns()

        fs_logger.info(
            "Fast Statistics (Operation Time: {fast_statistics_time:.3f}ms | Format Time: {format_time:.3f}ms): \n{fast_statistics}",
            fast_statistics_time = (fast_statistics_end_time - fast_statistics_start_time) / 1e6,
            format_time = (format_end_time - format_start_time) / 1e6,
            fast_statistics = "\n".join(buffer)
        )

        