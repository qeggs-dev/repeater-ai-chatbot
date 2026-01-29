# ==== 标准库 ==== #
import math
from datetime import datetime, timezone
from abc import ABC, abstractmethod
from typing import (
    Annotated
)

# ==== 第三方库 ==== #
import openai
from loguru import logger
import numpy as np

# ==== 自定义库 ==== #
from .._objects import (
    Request,
    Response,
)
from ....Coroutine_Pool import CoroutinePool
from TimeParser import (
    format_deltatime,
    format_deltatime_ns,
    format_time_duration_ns
)
from .._parser import (
    CallAPI,
    StreamAPI
)
from .._exceptions import *

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
    async def submit_Request(self, user_id:str, request: Request) -> Response:
        """提交请求，并等待API返回结果"""
        pass
    # endregion

    # region 预处理响应数据
    async def _preprocess_response(self, user_id: str, request: Request, response: Response):
        assert isinstance(user_id, str)
        assert isinstance(request, Request)
        assert isinstance(response, Response)

        if response.historical_context.last_content.reasoning_content:
            logger.info(
                "Reasoning_Content: \n{reasoning_content}",
                reasoning_content = request.context.last_content.reasoning_content,
                user_id = user_id,
                donot_send_console = True
            )
        if response.historical_context.last_content.content:
            logger.info(
                "Content: \n{content}",
                content = request.context.last_content.content,
                user_id = user_id,
                donot_send_console = True
            )
        
        await self._print_fast_statistics(
            user_id = user_id,
            request = request,
            response = response
        )
        return response
    # endregion

    # region 任务
    async def _submit_task(self, user_id: str, request: Request):
        assert isinstance(user_id, str), "user_id must be a string"
        assert isinstance(request, Request), "request must be a Request object"

        if request.stream:
            client = StreamAPI()
        else:
            client = CallAPI()
        try:
            return await client.call(
                user_id = user_id,
                request = request
            ), client
        except openai.BadRequestError as e:
            if e.code in range(400, 500):
                logger.error(f"BadRequestError: {e}", user_id = user_id)
                raise BadRequestError(e.message)
            elif e.code in range(500, 600):
                logger.error(f"API Server Error: {e}", user_id = user_id)
                raise APIServerError(e.message)
        except Exception as e:
            logger.error(f"Error: {e}", user_id = user_id)
            raise CallApiException(e)
    # endregion

    @staticmethod
    def _calculate_stability_cv(intervals: np.ndarray):
        """使用变异系数衡量数据稳定度"""
        assert isinstance(intervals, np.ndarray), "intervals Must be a numpy array"

        if len(intervals) == 0:
            return np.inf  # 无穷大表示不稳定
        
        std_dev = np.std(intervals)
        mean_val = np.mean(intervals)
        
        if mean_val == 0:
            return np.inf  # 防止除以零错误
        
        cv = std_dev / mean_val  # 变异系数
        stability = 1 / (1 + cv)  # 转换为稳定度分数 (0-1之间，越大越稳定)
        return float(stability)

    # region 打印日志
    async def _print_fast_statistics(self, user_id: str, request: Request, response: Response):
        """
        快速统计请求内容并输出到日志中

        :param user_id: 用户ID
        :param request: 请求对象
        :param response: 响应对象
        """
        assert isinstance(user_id, str), "user_id must be a string"
        assert isinstance(request, Request), "request must be a Request object"
        assert isinstance(response, Response), "response must be a Response object"

        logger.info("========== Fast Statistics =========", user_id = user_id)
        logger.info("Generating statistics...", user_id = user_id)
        logger.info("============= API INFO =============", user_id = user_id)
        logger.info(
            "API_URL: {url}",
            user_id = user_id,
            url = request.url,
        )
        logger.info(
            "Model: {model_id}",
            user_id = user_id,
            model_id = request.model
        )
        logger.info(
            "UserName: {user_name}",
            user_id = user_id,
            user_name = request.user_name
        )
        logger.info(
            "Chat Completion ID: {request_id}",
            user_id = user_id,
            request_id = response.id
        )
        logger.info(
            "Temperature: {temperature}",
            user_id = user_id,
            temperature = request.temperature
        )
        logger.info(
            "Top P: {top_p}",
            user_id = user_id,
            top_p = request.top_p
        )
        logger.info(
            "Frequency Penalty: {frequency_penalty}",
            user_id = user_id,
            frequency_penalty = request.frequency_penalty
        )
        logger.info(
            "Presence Penalty: {presence_penalty}",
            user_id = user_id,
            presence_penalty = request.presence_penalty
        )
        logger.info(
            "Max Tokens: {max_tokens}",
            user_id = user_id,
            max_tokens = request.max_tokens
        )
        logger.info(
            "Max Completion Tokens: {max_completion_tokens}",
            user_id = user_id,
            max_completion_tokens = request.max_completion_tokens
        )
        
        logger.info("============= Response =============", user_id = user_id)
        if response.system_fingerprint:
            logger.info(
                "System Fingerprint: {system_fingerprint}",
                user_id = user_id,
                system_fingerprint = response.system_fingerprint
            )
        logger.info(
            "Finish Reason: {finish_reason}",
            user_id = user_id,
            finish_reason = response.finish_reason
        )
        logger.info(
            "Finish Reason Cause: {finish_reason_cause}",
            user_id = user_id,
            finish_reason_cause = response.finish_reason_cause
        )

        if response.calling_log.total_chunk > 0:
            logger.info("============ Chunk Count ===========", user_id = user_id)
            logger.info(
                "Total Chunk: {total_chunk}",
                user_id = user_id,
                total_chunk = response.calling_log.total_chunk
            )
            if response.calling_log.empty_chunk > 0:
                logger.info(
                    "Empty Chunk: {empty_chunk}",
                    user_id = user_id,
                    empty_chunk = response.calling_log.empty_chunk
                )
                logger.info(
                    "Non-Empty Chunk: {non_empty_chunk}",
                    user_id = user_id,
                    non_empty_chunk = response.calling_log.total_chunk - response.calling_log.empty_chunk
                )
            logger.info(
                "Chunk effective ratio: {chunk_effective_ratio:.2%}",
                user_id = user_id,
                chunk_effective_ratio = 1 - response.calling_log.empty_chunk / response.calling_log.total_chunk
            )
        
        logger.info("========== Time Statistics =========", user_id = user_id)
        total_time = response.calling_log.stream_processing_end_time.monotonic - response.calling_log.request_start_time.monotonic
        logger.info(
            "Total Time: {total_time:.2f}s({format_time_duration})",
            user_id = user_id,
            total_time = total_time,
            format_time_duration = format_time_duration_ns(total_time, use_abbreviation=True)
        )
        requests_time = response.calling_log.request_end_time.monotonic - response.calling_log.request_start_time.monotonic
        logger.info(
            "API Request Time: {requests_time:.2f}s({format_time_duration})",
            user_id = user_id,
            requests_time = requests_time / 10**9,
            format_time_duration = format_time_duration_ns(requests_time, use_abbreviation=True)
        )
        stream_processing_time = response.calling_log.stream_processing_end_time.monotonic - response.calling_log.stream_processing_start_time.monotonic
        logger.info(
            "Stream Processing Time: {stream_processing_time:.2f}s({format_time_duration})",
            user_id = user_id,
            stream_processing_time = stream_processing_time / 10**9,
            format_time_duration = format_time_duration_ns(stream_processing_time, use_abbreviation=True)
        )

        created_utc_dt = datetime.fromtimestamp(response.created, tz=timezone.utc)
        created_utc_str = created_utc_dt.strftime("%Y-%m-%d %H:%M:%S (UTC)")
        logger.info(
            "Created Time: {created_utc_str}",
            user_id = user_id,
            created_utc_str = created_utc_str
        )

        created_local_dt = datetime.fromtimestamp(response.created)
        created_local_str = created_local_dt.strftime("%Y-%m-%d %H:%M:%S (Local)")
        logger.info(
            "Created Time: {created_local_str}",
            user_id = user_id,
            created_local_str = created_local_str
        )

        if response.calling_log.total_chunk > 0:
            timestamps = np.array([time.monotonic for time in response.calling_log.chunk_times], dtype=np.int64)
            time_differences = np.diff(timestamps)
            non_zero_time_differences = time_differences[time_differences != 0]
            max_chunk_spawn_time = int(np.max(time_differences))
            min_chunk_spawn_time = int(np.min(non_zero_time_differences))
            ave_chunk_spawn_time = int(np.mean(time_differences))
            chunk_generation_rate = 10**9 / ave_chunk_spawn_time
            chunk_stability_cv = self._calculate_stability_cv(time_differences)
            logger.info(
                "Chunk Generation Rate: {chunk_generation_rate:.2f} Chunks/s",
                user_id = user_id,
                chunk_generation_rate = chunk_generation_rate
            )
            logger.info(
                "Chunk Average Spawn Time: {ave_chunk_spawn_time:.2f}ms({format_time_duration})",
                user_id = user_id,
                ave_chunk_spawn_time = ave_chunk_spawn_time / 10**6,
                format_time_duration = format_time_duration_ns(ave_chunk_spawn_time, use_abbreviation=True)
            )
            logger.info(
                "Chunk Max Spawn Time: {max_chunk_spawn_time:.2f}ms({format_time_duration})",
                user_id = user_id,
                max_chunk_spawn_time = max_chunk_spawn_time / 10**6,
                format_time_duration = format_time_duration_ns(max_chunk_spawn_time, use_abbreviation=True)
            )
            logger.info(
                "Chunk Min Spawn Time: {min_chunk_spawn_time:.2f}ms({format_time_duration})",
                user_id = user_id,
                min_chunk_spawn_time = min_chunk_spawn_time / 10**6,
                format_time_duration = format_time_duration_ns(min_chunk_spawn_time, use_abbreviation=True)
            )
            logger.info(
                "Chunk time stability (Coefficient of Variation): {chunk_stability_cv}",
                user_id = user_id,
                chunk_stability_cv = chunk_stability_cv
            )

        logger.info("=========== Token Count ============", user_id = user_id)
        logger.info(
            "Total Tokens: {total_tokens}",
            user_id = user_id,
            total_tokens = response.token_usage.total_tokens
        )
        logger.info(
            "Context Input Tokens: {prompt_tokens}",
            user_id = user_id,
            prompt_tokens = response.token_usage.prompt_tokens
        )
        logger.info(
            "Completion Output Tokens: {completion_tokens}",
            user_id = user_id,
            completion_tokens = response.token_usage.completion_tokens
        )
        if response.token_usage.prompt_cache_hit_tokens is not None:
            logger.info(
                "Cache Hit Count: {prompt_cache_hit_tokens}",
                user_id = user_id,
                prompt_cache_hit_tokens = response.token_usage.prompt_cache_hit_tokens
            )
        if response.token_usage.prompt_cache_miss_tokens is not None:
            logger.info(
                "Cache Miss Count: {prompt_cache_miss_tokens}",
                user_id = user_id,
                prompt_cache_miss_tokens = response.token_usage.prompt_cache_miss_tokens
            )
        if not math.isnan(response.token_usage.cache_hit_ratio()):
            logger.info(
                "Cache Hit Ratio: {cache_hit_ratio:.2%}",
                user_id = user_id,
                cache_hit_ratio = response.token_usage.cache_hit_ratio()
            )
        if response.stream:
            logger.info(
                "Average Generation Rate: {avg_gen_rate:.2f} /s",
                user_id = user_id,
                avg_gen_rate = response.token_usage.completion_tokens / ((response.calling_log.stream_processing_end_time - response.calling_log.stream_processing_start_time) / 1e9)
            )

        logger.info("============= Content ==============", user_id = user_id)
        historical_context_text_length = response.historical_context.total_length
        new_context_text_length = response.new_context.total_length
        response.calling_log.reasoning_content_length = sum(len(content.reasoning_content) for content in response.new_context.context_list)
        response.calling_log.new_content_length = sum(len(content.content) for content in response.new_context.context_list)

        logger.info(
            "Total Content Length: {total_context_length}",
            user_id = user_id,
            total_context_length = historical_context_text_length + new_context_text_length
        )
        response.calling_log.total_context_length = response.historical_context.total_length
        logger.info(
            "New Reasoning Content Length: {reasoning_content_length}",
            user_id = user_id,
            reasoning_content_length = sum(len(content) for content in response.new_context.context_list)
        )
        logger.info(
            "New Answer Content Length: {new_content_length}",
            user_id = user_id,
            new_content_length = response.calling_log.new_content_length
        )
        logger.info(
            "Historical Context Text Length: {historical_context_length}",
            user_id = user_id,
            historical_context_length = historical_context_text_length
        )
        logger.info(
            "New Content Text Length: {new_context_length}",
            user_id = user_id,
            new_context_length = new_context_text_length
        )

        logger.info("====================================", user_id = user_id)