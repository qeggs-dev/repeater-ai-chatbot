# ==== 标准库 ==== #
import time
import math
from datetime import datetime, timezone
from abc import ABC, abstractmethod
from typing import (
    Annotated,
    Generator,
)

# ==== 第三方库 ==== #
from loguru import logger, Logger
import numpy as np

# ==== 自定义库 ==== #
from .._objects import (
    Request,
    Response,
    Runtime
)
from ....pools.awaitable_pool import CoroutinePool
from ....auxiliary.time import (
    format_time_duration_ns
)
from ....auxiliary.token import (
    format_token_duration
)
from ....request_log import RequestLog
from .._caller import (
    CallAPI,
    StreamAPI
)

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
            await self._print_fast_statistics(
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

    @staticmethod
    def _calculate_cv(intervals: np.ndarray[tuple[int], np.dtype[np.int64]]):
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
    
    @staticmethod
    def _calculate_interquartile_range(intervals: np.ndarray[tuple[int], np.dtype[np.int64]]):
        """使用四分位距衡量数据稳定性"""
        assert isinstance(intervals, np.ndarray), "intervals Must be a numpy array"

        if len(intervals) < 2:
            return np.inf
        
        q75, q25 = np.percentile(intervals, [75 ,25])
        iqr = float(q75 - q25)
        return iqr
    
    @staticmethod
    def _calculate_interdecile_range(intervals: np.ndarray[tuple[int], np.dtype[np.int64]]):
        """使用十分位距衡量数据稳定性"""
        assert isinstance(intervals, np.ndarray), "intervals Must be a numpy array"

        if len(intervals) < 2:
            return np.inf
        
        q90, q10 = np.percentile(intervals, [90 ,10])
        percentile_range = float(q90 - q10)
        return percentile_range
    
    @staticmethod
    def _calculate_mad(intervals: np.ndarray[tuple[int], np.dtype[np.int64]]):
        """使用平均绝对偏差衡量数据稳定性"""
        assert isinstance(intervals, np.ndarray), "intervals Must be a numpy array"

        if len(intervals) < 2:
            return np.inf

        mad = float(np.mean(np.abs(intervals - np.mean(intervals))))
        return mad
    
    @staticmethod
    def _fixed_length_sample(data: np.ndarray[tuple[int], np.dtype[np.int64]], target_length: int):
        """
        从可变长度数据中均匀采样固定长度
        """
        n = len(data)
        if n <= target_length:
            # 数据太短，直接返回原数据（或重复最后一个元素）
            return data.copy()
        
        # 生成均匀间隔的索引
        indices = np.linspace(0, n-1, target_length, dtype=int)
        return data[indices]
    
    @staticmethod
    def _min_max_normalize(arr: np.ndarray[tuple[int]]):
        return (arr - arr.min()) / (arr.max() - arr.min())
    
    @staticmethod
    def _parse_special_values(value) -> str:
        if value is None:
            return "No Set"
        elif isinstance(value, bool):
            return "Enabled" if value else "Disabled"
        else:
            return str(value)
    
    @classmethod
    def _draw_chart(cls, data: np.ndarray[tuple[int]], title: str, height: int = 5) -> Generator[str, None, None]:
        zoomed_data = cls._min_max_normalize(data) * height
        ctitle = f" {title} ".center(len(zoomed_data) + 2, "─")
        yield f"┌{ctitle}┐"
        for i in range(height - 1, -1, -1):
            text_buffer: list[str] = []
            for j in zoomed_data:
                if j - i > 1:
                    text_buffer.append("█")
                elif j - i > 0.75:
                    text_buffer.append("▓")
                elif j - i > 0.5:
                    text_buffer.append("▒")
                elif j - i > 0.25:
                    text_buffer.append("░")
                else:
                    text_buffer.append(" ")
            
                charts = "".join(text_buffer)
                yield f"│ {charts} │"
        end_line = "─" * (len(zoomed_data) + 2)
        yield f"└{end_line}┘"
    
    @staticmethod
    def _calculate_skewness(data: np.ndarray[tuple[int]]) -> float:
        n = len(data)
        mean = np.mean(data)
        # 计算中心矩
        m2 = np.sum((data - mean) ** 2) / n      # 二阶矩
        m3 = np.sum((data - mean) ** 3) / n      # 三阶矩
        # 修正后的样本偏度
        g1 = m3 / (m2 ** 1.5)
        # 小样本修正因子
        correction = np.sqrt(n * (n - 1)) / (n - 2)
        return g1 * correction
    
    @staticmethod
    def _calculate_kurtosis(data: np.ndarray[tuple[int]]) -> np.float64:
        n = len(data)
        mean = np.mean(data)
        variance = np.var(data) # 注意：这是有偏的总体方差
        # 计算四阶中心矩并除以方差平方，最后减去3得到超额峰度
        kurtosis = np.sum((data - mean) ** 4 / (variance ** 2)) / n - 3
        return kurtosis

    @staticmethod
    def _calculate_entropy(data: np.ndarray[tuple[int]]) -> np.float64:
        # 1. 统计每个唯一值出现的次数
        _, counts = np.unique(data, return_counts=True)
        # 2. 计算每个值的概率
        probabilities = counts / len(data)
        # 3. 计算熵: -sum(p * log2(p))
        # 添加一个极小值 np.finfo(float).eps 防止概率为0时出现 log(0) 的警告
        entropy = -np.sum(probabilities * np.log2(probabilities + np.finfo(float).eps))
        return entropy
    
    @staticmethod
    def _format_timedelta(
        timedelta: int | float,
    ) -> str:
        return f"{timedelta / 1e6:.2f}ms({format_time_duration_ns(timedelta, use_abbreviation=True)})"
    
    
    @staticmethod
    def _format_token(
        token_count: int,
    ) -> str:
        return f"{token_count}({format_token_duration(token_count, use_abbreviation=True, delimiter = ' ')}Tokens)"
    
    @classmethod
    def _chunk_statistics(
        cls,
        name: str,
        request_log: RequestLog,
        raw_timestamps: list[int],
        raw_queue_backlogs: list[int] | None = None,
        title_width: int = 36,
    ) -> Generator[str, None, None]:
        title = f"{name} Chunk Statistics"
        dividing_line_length = title_width - len(title) - 2
        if dividing_line_length % 2 == 0:
            dividing_line_prefix = "-" * (dividing_line_length // 2)
            dividing_line_suffix = dividing_line_prefix
        else:
            dividing_line_prefix = "-" * (dividing_line_length // 2)
            dividing_line_suffix = "-" * (dividing_line_length // 2 + 1)
        yield f"{dividing_line_prefix} {title} {dividing_line_suffix}"
        timestamps = np.array(raw_timestamps, dtype=np.int64)
        time_differences = np.diff(timestamps)
        non_zero_time_differences = time_differences[time_differences != 0]
        stream_processing_time = request_log.stream_processing_end_time.monotonic - request_log.stream_processing_start_time.monotonic
        if time_differences.size > 0 and non_zero_time_differences.size > 0:

            max_chunk_spawn_time = int(np.max(time_differences))
            min_chunk_spawn_time = int(np.min(non_zero_time_differences))
            ave_chunk_spawn_time = float(np.mean(time_differences))
            chunk_median_time = float(np.median(time_differences))
            chunk_spawn_time_std = float(np.std(time_differences))
            chunk_spawn_time_iqr = cls._calculate_interquartile_range(time_differences)
            chunk_spawn_time_idr = cls._calculate_interdecile_range(time_differences)
            chunk_spawn_time_mad = cls._calculate_mad(time_differences)
            chunk_spawn_time_relative_mad = chunk_spawn_time_mad / chunk_median_time
            chunk_generation_rate = request_log.total_chunk / (stream_processing_time / 1e9)
            chunk_stability_cv = cls._calculate_cv(time_differences)
            simple_chunk_times = cls._fixed_length_sample(time_differences, 34)
            first_chunk_wait_time = raw_timestamps[0] - request_log.stream_processing_start_time.monotonic
            skewness = cls._calculate_skewness(time_differences)
            kurtosis = cls._calculate_kurtosis(time_differences)
            entropy = cls._calculate_entropy(time_differences)

            yield from cls._draw_chart(
                simple_chunk_times,
                title = f"{name} Chunk Times",
            )
            yield f"{name} Chunk Rate: {chunk_generation_rate:.2f} Chunks/s"
            yield f"{name} First Chunk Wait Time: {cls._format_timedelta(first_chunk_wait_time)}"
            yield f"{name} Chunk Average Time: {cls._format_timedelta(ave_chunk_spawn_time)}"
            yield f"{name} Chunk Max Time: {cls._format_timedelta(max_chunk_spawn_time)}"
            yield f"{name} Chunk Min Time: {cls._format_timedelta(min_chunk_spawn_time)}"
            yield f"{name} Chunk Time CV: {chunk_stability_cv:.2%}"
            yield f"{name} Chunk Time Range: {cls._format_timedelta((max_chunk_spawn_time - min_chunk_spawn_time))}"
            yield f"{name} Chunk Time Median: {cls._format_timedelta(chunk_median_time)}"
            yield f"{name} Chunk Time STD: {cls._format_timedelta(chunk_spawn_time_std)}"
            yield f"{name} Chunk Time MAD: {cls._format_timedelta(chunk_spawn_time_mad)})"
            yield f"{name} Chunk Time Relative MAD: {chunk_spawn_time_relative_mad:.2%}"
            yield f"{name} Chunk Time IQR: {cls._format_timedelta(chunk_spawn_time_iqr)}"
            yield f"{name} Chunk Time IDR: {cls._format_timedelta(chunk_spawn_time_idr)}"
            yield f"{name} Chunk Time Skewness: {skewness:.2%}"
            yield f"{name} Chunk Time Kurtosis: {kurtosis:.2%}"
            yield f"{name} Chunk Time Entropy: {entropy:.2%}"

            if raw_queue_backlogs is not None:
                queue_backlog = np.array(raw_queue_backlogs, dtype=np.int64)
                max_queue_backlog = int(np.max(queue_backlog))
                min_queue_backlog = int(np.min(queue_backlog))
                avg_queue_backlog = int(np.mean(queue_backlog))
                median_queue_backlog = float(np.median(queue_backlog))
                queue_backlog_std = float(np.std(queue_backlog))
                queue_backlog_iqr = cls._calculate_interquartile_range(queue_backlog)
                queue_backlog_idr = cls._calculate_interdecile_range(queue_backlog)
                queue_backlog_mad = cls._calculate_mad(queue_backlog)
                queue_backlog_relative_mad = queue_backlog_mad / median_queue_backlog
                queue_backlog_cv = cls._calculate_cv(queue_backlog)
                queue_backlog_skewness = cls._calculate_skewness(queue_backlog)
                queue_backlog_kurtosis = cls._calculate_kurtosis(queue_backlog)
                queue_backlog_entropy = cls._calculate_entropy(queue_backlog)

                yield f"{name} Max Queue Backlog: {max_queue_backlog}"
                yield f"{name} Min Queue Backlog: {min_queue_backlog}"
                yield f"{name} Avg Queue Backlog: {avg_queue_backlog:.2f}"
                yield f"{name} Queue Backlog CV: {queue_backlog_cv:.2%}"
                yield f"{name} Queue Backlog Median: {median_queue_backlog}"
                yield f"{name} Queue Backlog STD: {queue_backlog_std:.2f}"
                yield f"{name} Queue Backlog MAD: {queue_backlog_mad:.2f}"
                yield f"{name} Queue Backlog Relative MAD: {queue_backlog_relative_mad:.2%}"
                yield f"{name} Queue Backlog IQR: {queue_backlog_iqr}"
                yield f"{name} Queue Backlog IDR: {queue_backlog_idr}"
                yield f"{name} Queue Backlog Skewness: {queue_backlog_skewness:.2%}"
                yield f"{name} Queue Backlog Kurtosis: {queue_backlog_kurtosis:.2%}"
                yield f"{name} Queue Backlog Entropy: {queue_backlog_entropy:.2%}"

    def _gen_fast_statistics(self, user_id: str, request: Request, response: Response) -> Generator[str, None, None]:
        """
        快速统计请求内容并生成字符串

        :param user_id: 用户ID
        :param request: 请求对象
        :param response: 响应对象
        """
        yield "========== Fast Statistics ========="
        yield "Generating statistics..."
        yield "============= API INFO ============="
        yield f"API URL: {request.url}"
        yield f"Model: {request.model}"
        yield f"User Name: {request.user_name}"
        yield f"Task ID: {response.request_log.task_id}"
        yield f"Response ID: {response.id}"
        yield f"Thinking: {self._parse_special_values(request.thinking)}"
        yield f"Seed: {self._parse_special_values(request.seed)}"
        yield f"Temperature: {self._parse_special_values(request.temperature)}"
        yield f"Top A: {self._parse_special_values(request.top_a)}"
        yield f"Top P: {self._parse_special_values(request.top_p)}"
        yield f"Top K: {self._parse_special_values(request.top_k)}"
        yield f"Repetition Penalty: {self._parse_special_values(request.repetition_penalty)}"
        yield f"Frequency Penalty: {self._parse_special_values(request.frequency_penalty)}"
        yield f"Presence Penalty: {self._parse_special_values(request.presence_penalty)}"
        yield f"Max Tokens: {self._parse_special_values(request.max_tokens)}"
        yield f"Max Completion Tokens: {self._parse_special_values(request.max_completion_tokens)}"
        if request.fim_mode:
            yield "Completion Mode: FIM"
            yield f"FIM Echo: {self._parse_special_values(request.echo)}"
        else:
            yield "Completion Mode: Chat"
        
        if not request.remove_reasoning_prompt:
            yield "Reasoning Prompt: Retained"
        else:
            yield "Reasoning Prompt: Removed"
        
        yield "============= Response ============="
        if response.system_fingerprint:
            yield f"System Fingerprint: {response.system_fingerprint}"
        yield f"Finish Reason: {response.finish_reason}"
        yield f"Finish Reason Cause: {response.finish_reason_cause}"

        if response.request_log.total_chunk > 0:
            yield "============ Chunk Count ==========="
            yield f"Total Chunk: {response.request_log.total_chunk}"
            if response.request_log.empty_chunk > 0:
                yield f"Empty Chunk: {response.request_log.empty_chunk}"
                yield f"Non-Empty Chunk: {response.request_log.total_chunk - response.request_log.empty_chunk}"
            yield f"Chunk effective ratio: {1 - response.request_log.empty_chunk / response.request_log.total_chunk:.2%}"
        
        yield f"========== Time Statistics ========="
        
        total_time = response.request_log.stream_processing_end_time.monotonic - response.request_log.request_start_time.monotonic
        yield f"Total Time: {self._format_timedelta(total_time)}"

        preprocessing_time = response.request_log.prepare_end_time.monotonic - response.request_log.prepare_start_time.monotonic
        yield f"Preprocessing Time: {self._format_timedelta(preprocessing_time)}"

        requests_time = response.request_log.request_end_time.monotonic - response.request_log.request_start_time.monotonic
        yield f"API Request Time: {self._format_timedelta(requests_time)}"

        stream_processing_time = response.request_log.stream_processing_end_time.monotonic - response.request_log.stream_processing_start_time.monotonic
        yield f"Stream Processing Time: {self._format_timedelta(stream_processing_time)}"

        if response.token_usage is not None:
            generation_speed = response.token_usage.completion_tokens / (stream_processing_time / 1e9)
            yield f"Generation Speed: {generation_speed:.2f} Tokens/s"

        created_utc_dt = datetime.fromtimestamp(response.created, tz=timezone.utc)
        created_utc_str = created_utc_dt.strftime("%Y-%m-%d %H:%M:%S (UTC)")
        yield f"Created Time: {created_utc_str}"

        created_local_dt = datetime.fromtimestamp(response.created)
        created_local_str = created_local_dt.strftime("%Y-%m-%d %H:%M:%S (Local)")
        yield f"Created Time: {created_local_str}"

        if response.request_log.total_chunk > 0:
            if response.request_log.chunk_generated_times:
                yield from self._chunk_statistics(
                    "Generated",
                    request_log = response.request_log,
                    raw_timestamps = [timestamp.monotonic for timestamp in response.request_log.chunk_generated_times]
                )
        
            if response.request_log.chunk_generated_times:
                yield from self._chunk_statistics(
                    "Translation",
                    request_log = response.request_log,
                    raw_timestamps = [timestamp.monotonic for timestamp in response.request_log.translation_chunk_times],
                    raw_queue_backlogs = response.request_log.translation_queue_backlog
                )
        
            if response.request_log.chunk_times:
                yield from self._chunk_statistics(
                    "Transmitted",
                    request_log = response.request_log,
                    raw_timestamps = [timestamp.monotonic for timestamp in response.request_log.chunk_times],
                    raw_queue_backlogs = response.request_log.queue_backlog
                )

        if response.token_usage is not None:
            yield f"=========== Token Count ============"
            yield f"Total Tokens: {self._format_token(response.token_usage.total_tokens)}"
            yield f"Context Input Tokens: {self._format_token(response.token_usage.prompt_tokens)}"

            if response.token_usage.prompt_cache_hit_tokens is not None:
                yield f"Cache Hit Tokens: {self._format_token(response.token_usage.prompt_cache_hit_tokens)}"
            if response.token_usage.prompt_cache_miss_tokens is not None:
                yield f"Cache Miss Tokens: {self._format_token(response.token_usage.prompt_cache_miss_tokens)}"

            yield f"Completion Output Tokens: {self._format_token(response.token_usage.completion_tokens)}"
            
            if not math.isnan(response.token_usage.cache_hit_ratio()):
                yield f"Cache Hit Ratio: {response.token_usage.cache_hit_ratio():.2%}"
            
            if response.stream and response.request_log.chunk_times:
                if len(response.request_log.chunk_times) > 1:
                    avg_gen_rate = response.token_usage.completion_tokens / (
                        (
                            response.request_log.chunk_times[-1].monotonic -
                            response.request_log.chunk_times[0].monotonic
                        ) / 1e9
                    )
                    yield f"Average Generation Rate: {avg_gen_rate:.2f} Token/s"

        yield "============= Content =============="
        historical_context_text_length = response.historical_context.total_length
        new_context_text_length = response.new_context.total_length
        response.request_log.reasoning_content_length = sum(len(content.reasoning_content) for content in response.new_context.context_list if content.reasoning_content)
        response.request_log.new_content_length = sum(len(content.content) for content in response.new_context.context_list)
        total_context_length = historical_context_text_length + new_context_text_length
        reasoning_content_length = response.request_log.reasoning_content_length
        new_content_length = response.request_log.new_content_length
        historical_context_length = historical_context_text_length
        new_context_length = new_context_text_length
        

        yield f"Total Content Length: {total_context_length}"
        yield f"New Reasoning Content Length: {reasoning_content_length}"
        yield f"New Answer Content Length: {new_content_length}"
        yield f"Historical Context Text Length: {historical_context_length}"
        yield f"New Content Text Length: {new_context_length}"

        yield f"===================================="

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

        fs_logger = logger.bind(user_id = user_id)

        buffer: list[str] = []

        fast_statistics_start_time = time.perf_counter_ns()
        buffer.extend(
            self._gen_fast_statistics(
                user_id = user_id,
                request = request,
                response = response,
            )
        )
        fast_statistics_end_time = time.perf_counter_ns()

        fs_logger.info(
            "Fast Statistics (Time: {fast_statistics_time:.3f}ms): \n{fast_statistics}",
            fast_statistics_time = (fast_statistics_end_time - fast_statistics_start_time) / 1e6,
            fast_statistics = "\n".join(buffer)
        )

        