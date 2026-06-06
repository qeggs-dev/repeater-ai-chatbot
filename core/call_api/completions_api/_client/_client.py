# ==== 标准库 ==== #
import math
from datetime import datetime, timezone
from abc import ABC, abstractmethod
from typing import (
    Annotated
)

# ==== 第三方库 ==== #
from loguru import logger
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
            if response.new_context.last_content.reasoning_content:
                logger.info(
                    "Reasoning_Content: \n\n{reasoning_content}\n",
                    reasoning_content = response.new_context.last_content.reasoning_content,
                    user_id = user_id,
                    donot_send_console = True
                )
            if response.new_context.last_content.content:
                logger.info(
                    "Content: \n\n{content}\n",
                    content = response.new_context.last_content.content,
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
    async def _submit_task(self, user_id: str, request: Request):
        assert isinstance(user_id, str), "user_id must be a string"
        assert isinstance(request, Request), "request must be a Request object"

        if request.stream:
            client = StreamAPI()
        else:
            client = CallAPI()
        return await client.call(
            user_id = user_id,
            request = request
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
    def _draw_chart(cls, fs_logger, data: np.ndarray[tuple[int]], ctitle: str, height: int = 5):
        zoomed_data = cls._min_max_normalize(data) * height
        fs_logger.info(
            "┌{charts}┐",
            charts = f" {ctitle} ".center(len(zoomed_data) + 2, "─"),
        )
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
            fs_logger.info(
                "│ {charts} │",
                charts = "".join(text_buffer)
            )
        fs_logger.info(
            "└{charts}┘",
            charts = "─" * (len(zoomed_data) + 2)
        )
    
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

        fs_logger.info("========== Fast Statistics =========")
        fs_logger.info("Generating statistics...")
        fs_logger.info("============= API INFO =============")
        fs_logger.info(
            "API URL: {url}",
            url = request.url,
        )
        fs_logger.info(
            "Model: {model_id}",
            model_id = request.model
        )
        fs_logger.info(
            "User Name: {user_name}",
            user_name = request.user_name
        )
        fs_logger.info(
            "Task ID: {task_id}",
            task_id = response.request_log.task_id
        )
        fs_logger.info(
            "Response ID: {request_id}",
            request_id = response.id
        )
        fs_logger.info(
            "Thinking: {thinking}",
            thinking = self._parse_special_values(request.thinking)
        )
        fs_logger.info(
            "Seed: {seed}",
            seed = self._parse_special_values(request.seed)
        )
        fs_logger.info(
            "Temperature: {temperature}",
            temperature = self._parse_special_values(request.temperature)
        )
        fs_logger.info(
            "Top A: {top_p}",
            top_p = self._parse_special_values(request.top_a)
        )
        fs_logger.info(
            "Top P: {top_p}",
            top_p = self._parse_special_values(request.top_p)
        )
        fs_logger.info(
            "Top K: {top_k}",
            top_k = self._parse_special_values(request.top_k)
        )
        fs_logger.info(
            "Repetition Penalty: {repetition_penalty}",
            repetition_penalty = self._parse_special_values(request.repetition_penalty)
        )
        fs_logger.info(
            "Frequency Penalty: {frequency_penalty}",
            frequency_penalty = self._parse_special_values(request.frequency_penalty)
        )
        fs_logger.info(
            "Presence Penalty: {presence_penalty}",
            presence_penalty = self._parse_special_values(request.presence_penalty)
        )
        fs_logger.info(
            "Max Tokens: {max_tokens}",
            max_tokens = self._parse_special_values(request.max_tokens)
        )
        fs_logger.info(
            "Max Completion Tokens: {max_completion_tokens}",
            max_completion_tokens = self._parse_special_values(request.max_completion_tokens)
        )
        if request.fim_mode:
            fs_logger.info("Completion Mode: FIM")
            fs_logger.info(
                "FIM Echo: {fim_echo}",
                fim_echo = self._parse_special_values(request.echo)
            )
        else:
            fs_logger.info("Completion Mode: Chat")
        
        if not request.remove_reasoning_prompt:
            fs_logger.info("Reasoning Prompt: Retained")
        else:
            fs_logger.info("Reasoning Prompt: Removed")
        
        fs_logger.info("============= Response =============")
        if response.system_fingerprint:
            fs_logger.info(
                "System Fingerprint: {system_fingerprint}",
                system_fingerprint = response.system_fingerprint
            )
        fs_logger.info(
            "Finish Reason: {finish_reason}",
            finish_reason = response.finish_reason
        )
        fs_logger.info(
            "Finish Reason Cause: {finish_reason_cause}",
            finish_reason_cause = response.finish_reason_cause
        )

        if response.request_log.total_chunk > 0:
            fs_logger.info("============ Chunk Count ===========")
            fs_logger.info(
                "Total Chunk: {total_chunk}",
                total_chunk = response.request_log.total_chunk
            )
            if response.request_log.empty_chunk > 0:
                fs_logger.info(
                    "Empty Chunk: {empty_chunk}",
                    empty_chunk = response.request_log.empty_chunk
                )
                fs_logger.info(
                    "Non-Empty Chunk: {non_empty_chunk}",
                    non_empty_chunk = response.request_log.total_chunk - response.request_log.empty_chunk
                )
            fs_logger.info(
                "Chunk effective ratio: {chunk_effective_ratio:.2%}",
                chunk_effective_ratio = 1 - response.request_log.empty_chunk / response.request_log.total_chunk
            )
        
        fs_logger.info("========== Time Statistics =========")
        
        total_time = response.request_log.stream_processing_end_time.monotonic - response.request_log.request_start_time.monotonic
        fs_logger.info(
            "Total Time: {total_time:.2f}s({format_time_duration})",
            total_time = total_time / 1e9,
            format_time_duration = format_time_duration_ns(total_time, use_abbreviation=True)
        )

        preprocessing_time = response.request_log.prepare_end_time.monotonic - response.request_log.prepare_start_time.monotonic
        fs_logger.info(
            "Preprocessing Time: {preprocessing_time:.2f}ms({format_time_duration})",
            preprocessing_time = preprocessing_time / 1e6,
            format_time_duration = format_time_duration_ns(preprocessing_time, use_abbreviation=True)
        )

        requests_time = response.request_log.request_end_time.monotonic - response.request_log.request_start_time.monotonic
        fs_logger.info(
            "API Request Time: {requests_time:.2f}ms({format_time_duration})",
            requests_time = requests_time / 1e6,
            format_time_duration = format_time_duration_ns(requests_time, use_abbreviation=True)
        )

        stream_processing_time = response.request_log.stream_processing_end_time.monotonic - response.request_log.stream_processing_start_time.monotonic
        fs_logger.info(
            "Stream Processing Time: {stream_processing_time:.2f}s({format_time_duration})",
            stream_processing_time = stream_processing_time / 1e9,
            format_time_duration = format_time_duration_ns(stream_processing_time, use_abbreviation=True)
        )

        fs_logger.info(
            "Generation Speed: {generation_speed:.2f} Tokens/s",
            generation_speed = response.token_usage.completion_tokens / (stream_processing_time / 1e9)
        )

        created_utc_dt = datetime.fromtimestamp(response.created, tz=timezone.utc)
        created_utc_str = created_utc_dt.strftime("%Y-%m-%d %H:%M:%S (UTC)")
        fs_logger.info(
            "Created Time: {created_utc_str}",
            created_utc_str = created_utc_str
        )

        created_local_dt = datetime.fromtimestamp(response.created)
        created_local_str = created_local_dt.strftime("%Y-%m-%d %H:%M:%S (Local)")
        fs_logger.info(
            "Created Time: {created_local_str}",
            created_local_str = created_local_str
        )

        if response.request_log.total_chunk > 0:
            if response.request_log.chunk_generated_times:
                fs_logger.info("==== Generated Chunk Statistics ====")
                raw_timestamps = [time.monotonic for time in response.request_log.chunk_generated_times]
                timestamps = np.array(raw_timestamps, dtype=np.int64)
                time_differences = np.diff(timestamps)
                non_zero_time_differences = time_differences[time_differences != 0]
                if time_differences.size > 0 and non_zero_time_differences.size > 0:
                    max_chunk_spawn_time = int(np.max(time_differences))
                    min_chunk_spawn_time = int(np.min(non_zero_time_differences))
                    ave_chunk_spawn_time = float(np.mean(time_differences))
                    chunk_median_time = float(np.median(time_differences))
                    chunk_spawn_time_std = float(np.std(time_differences))
                    chunk_spawn_time_iqr = self._calculate_interquartile_range(time_differences)
                    chunk_spawn_time_idr = self._calculate_interdecile_range(time_differences)
                    chunk_spawn_time_mad = self._calculate_mad(time_differences)
                    chunk_spawn_time_relative_mad = chunk_spawn_time_mad / chunk_median_time
                    chunk_generation_rate = response.request_log.total_chunk / (stream_processing_time / 1e9)
                    chunk_stability_cv = self._calculate_cv(time_differences)
                    simple_chunk_times = self._fixed_length_sample(time_differences, 34)
                    first_chunk_wait_time = raw_timestamps[0] - response.request_log.stream_processing_start_time.monotonic
                    skewness = self._calculate_skewness(time_differences)
                    self._draw_chart(
                        fs_logger,
                        simple_chunk_times,
                        ctitle = "Generated Chunk Times"
                    )
                    fs_logger.info(
                        "Generated Chunk Rate: {chunk_generation_rate:.2f} Chunks/s",
                        chunk_generation_rate = chunk_generation_rate
                    )
                    fs_logger.info(
                        "First Generated Chunk Wait Time: {chunk_wait_time:.2f}ms({format_time_duration})",
                        chunk_wait_time = first_chunk_wait_time / 1e6,
                        format_time_duration = format_time_duration_ns(first_chunk_wait_time, use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Generated Chunk Average Time: {ave_chunk_spawn_time:.2f}ms({format_time_duration})",
                        ave_chunk_spawn_time = ave_chunk_spawn_time / 1e6,
                        format_time_duration = format_time_duration_ns(int(ave_chunk_spawn_time), use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Generated Chunk Max Time: {max_chunk_spawn_time:.2f}ms({format_time_duration})",
                        max_chunk_spawn_time = max_chunk_spawn_time / 1e6,
                        format_time_duration = format_time_duration_ns(max_chunk_spawn_time, use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Generated Chunk Min Time: {min_chunk_spawn_time:.2f}ms({format_time_duration})",
                        min_chunk_spawn_time = min_chunk_spawn_time / 1e6,
                        format_time_duration = format_time_duration_ns(min_chunk_spawn_time, use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Generated Chunk Time CV: {chunk_stability_cv:.2%}",
                        chunk_stability_cv = chunk_stability_cv,
                    )
                    fs_logger.info(
                        "Generated Chunk Time Range: {chunk_stability_range:.2f}ms({format_time_duration})",
                        chunk_stability_range = (max_chunk_spawn_time - min_chunk_spawn_time) / 1e6,
                        format_time_duration = format_time_duration_ns(max_chunk_spawn_time - min_chunk_spawn_time, use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Generated Chunk Time Median: {chunk_median_time:.2f}ms({format_time_duration})",
                        chunk_median_time = chunk_median_time / 1e6,
                        format_time_duration = format_time_duration_ns(int(chunk_median_time), use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Generated Chunk Time STD: {chunk_std_time:.2f}ms({format_time_duration})",
                        chunk_std_time = chunk_spawn_time_std / 1e6,
                        format_time_duration = format_time_duration_ns(int(chunk_spawn_time_std), use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Generated Chunk Time MAD: {chunk_mad_time:.2f}ms({format_time_duration})",
                        chunk_mad_time = chunk_spawn_time_mad / 1e6,
                        format_time_duration = format_time_duration_ns(int(chunk_spawn_time_mad), use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Generated Chunk Time Relative MAD: {chunk_relative_time_mad:.2%}",
                        chunk_relative_time_mad = chunk_spawn_time_relative_mad
                    )
                    fs_logger.info(
                        "Generated Chunk Time IQR: {chunk_iqr_time:.2f}ms({format_time_duration})",
                        chunk_iqr_time = chunk_spawn_time_iqr / 1e6,
                        format_time_duration = format_time_duration_ns(int(chunk_spawn_time_iqr), use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Generated Chunk Time IDR: {chunk_idr_time:.2f}ms({format_time_duration})",
                        chunk_idr_time = chunk_spawn_time_idr / 1e6,
                        format_time_duration = format_time_duration_ns(int(chunk_spawn_time_idr), use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Generated Chunk Time Skewness {chunk_time_skewness:.4f}",
                        chunk_time_skewness = skewness
                    )
        
        if response.request_log.total_chunk > 0:
            if response.request_log.chunk_generated_times:
                fs_logger.info("=== Translation Chunk Statistics ===")
                raw_timestamps = [time.monotonic for time in response.request_log.translation_chunk_times]
                raw_queue_backlog = response.request_log.processor_queue_backlog
                timestamps = np.array(raw_timestamps, dtype=np.int64)
                queue_backlog = np.array(raw_queue_backlog, dtype=np.int64)
                time_differences = np.diff(timestamps)
                non_zero_time_differences = time_differences[time_differences != 0]
                if time_differences.size > 0 and non_zero_time_differences.size > 0:
                    max_chunk_spawn_time = int(np.max(time_differences))
                    min_chunk_spawn_time = int(np.min(non_zero_time_differences))
                    ave_chunk_spawn_time = float(np.mean(time_differences))
                    chunk_median_time = float(np.median(time_differences))
                    chunk_spawn_time_std = float(np.std(time_differences))
                    chunk_spawn_time_iqr = self._calculate_interquartile_range(time_differences)
                    chunk_spawn_time_idr = self._calculate_interdecile_range(time_differences)
                    chunk_spawn_time_mad = self._calculate_mad(time_differences)
                    chunk_spawn_time_relative_mad = chunk_spawn_time_mad / chunk_median_time
                    chunk_generation_rate = response.request_log.total_chunk / (stream_processing_time / 1e9)
                    chunk_stability_cv = self._calculate_cv(time_differences)
                    simple_chunk_times = self._fixed_length_sample(time_differences, 34)
                    first_chunk_wait_time = raw_timestamps[0] - response.request_log.stream_processing_start_time.monotonic
                    skewness = self._calculate_skewness(time_differences)
                    self._draw_chart(
                        fs_logger,
                        simple_chunk_times,
                        ctitle = "Translation Chunk Times",
                    )
                    fs_logger.info(
                        "Translation Chunk Rate: {chunk_generation_rate:.2f} Chunks/s",
                        chunk_generation_rate = chunk_generation_rate
                    )
                    fs_logger.info(
                        "Translation First Chunk Wait Time: {chunk_wait_time:.2f}ms({format_time_duration})",
                        chunk_wait_time = first_chunk_wait_time / 1e6,
                        format_time_duration = format_time_duration_ns(first_chunk_wait_time, use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Translation Chunk Average Time: {ave_chunk_spawn_time:.2f}ms({format_time_duration})",
                        ave_chunk_spawn_time = ave_chunk_spawn_time / 1e6,
                        format_time_duration = format_time_duration_ns(int(ave_chunk_spawn_time), use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Translation Chunk Max Time: {max_chunk_spawn_time:.2f}ms({format_time_duration})",
                        max_chunk_spawn_time = max_chunk_spawn_time / 1e6,
                        format_time_duration = format_time_duration_ns(max_chunk_spawn_time, use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Translation Chunk Min Time: {min_chunk_spawn_time:.2f}ms({format_time_duration})",
                        min_chunk_spawn_time = min_chunk_spawn_time / 1e6,
                        format_time_duration = format_time_duration_ns(min_chunk_spawn_time, use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Translation Chunk Time CV: {chunk_stability_cv:.2%}",
                        chunk_stability_cv = chunk_stability_cv,
                    )
                    fs_logger.info(
                        "Translation Chunk Time Range: {chunk_stability_range:.2f}ms({format_time_duration})",
                        chunk_stability_range = (max_chunk_spawn_time - min_chunk_spawn_time) / 1e6,
                        format_time_duration = format_time_duration_ns(max_chunk_spawn_time - min_chunk_spawn_time, use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Translation Chunk Time Median: {chunk_median_time:.2f}ms({format_time_duration})",
                        chunk_median_time = chunk_median_time / 1e6,
                        format_time_duration = format_time_duration_ns(int(chunk_median_time), use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Translation Chunk Time STD: {chunk_std_time:.2f}ms({format_time_duration})",
                        chunk_std_time = chunk_spawn_time_std / 1e6,
                        format_time_duration = format_time_duration_ns(int(chunk_spawn_time_std), use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Translation Chunk Time MAD: {chunk_mad_time:.2f}ms({format_time_duration})",
                        chunk_mad_time = chunk_spawn_time_mad / 1e6,
                        format_time_duration = format_time_duration_ns(int(chunk_spawn_time_mad), use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Translation Chunk Time Relative MAD: {chunk_relative_time_mad:.2%}",
                        chunk_relative_time_mad = chunk_spawn_time_relative_mad
                    )
                    fs_logger.info(
                        "Translation Chunk Time IQR: {chunk_iqr_time:.2f}ms({format_time_duration})",
                        chunk_iqr_time = chunk_spawn_time_iqr / 1e6,
                        format_time_duration = format_time_duration_ns(int(chunk_spawn_time_iqr), use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Translation Chunk Time IDR: {chunk_idr_time:.2f}ms({format_time_duration})",
                        chunk_idr_time = chunk_spawn_time_idr / 1e6,
                        format_time_duration = format_time_duration_ns(int(chunk_spawn_time_idr), use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Translation Chunk Time Skewness {chunk_time_skewness:.4f}",
                        chunk_time_skewness = skewness
                    )
                    fs_logger.info(
                        "Translation Max Queue Backlog: {max_queue_backlog}",
                        max_queue_backlog = queue_backlog.max()
                    )
                    fs_logger.info(
                        "Translation Min Queue Backlog: {min_queue_backlog}",
                        min_queue_backlog = queue_backlog.min()
                    )
                    fs_logger.info(
                        "Translation Mean Queue Backlog: {mean_queue_backlog:.4f}",
                        mean_queue_backlog = queue_backlog.mean()
                    )
                    fs_logger.info(
                        "Translation Median Queue Backlog: {median_queue_backlog:.4f}",
                        median_queue_backlog = np.median(queue_backlog)
                    )
        
            if response.request_log.chunk_times:
                fs_logger.info("====== Parsed Chunk Statistics =====")
                raw_timestamps = [time.monotonic for time in response.request_log.chunk_times]
                raw_queue_backlog = response.request_log.processor_queue_backlog
                timestamps = np.array(raw_timestamps, dtype=np.int64)
                queue_backlog = np.array(raw_queue_backlog, dtype=np.int64)
                time_differences = np.diff(timestamps)
                non_zero_time_differences = time_differences[time_differences != 0]
                if time_differences.size > 0 and non_zero_time_differences.size > 0:
                    max_chunk_spawn_time = int(np.max(time_differences))
                    min_chunk_spawn_time = int(np.min(non_zero_time_differences))
                    ave_chunk_spawn_time = float(np.mean(time_differences))
                    chunk_median_time = float(np.median(time_differences))
                    chunk_spawn_time_std = float(np.std(time_differences))
                    chunk_spawn_time_iqr = self._calculate_interquartile_range(time_differences)
                    chunk_spawn_time_idr = self._calculate_interdecile_range(time_differences)
                    chunk_spawn_time_mad = self._calculate_mad(time_differences)
                    chunk_spawn_time_relative_mad = chunk_spawn_time_mad / chunk_median_time
                    chunk_generation_rate = response.request_log.total_chunk / (stream_processing_time / 1e9)
                    chunk_stability_cv = self._calculate_cv(time_differences)
                    simple_chunk_times = self._fixed_length_sample(time_differences, 34)
                    first_chunk_wait_time = raw_timestamps[0] - response.request_log.stream_processing_start_time.monotonic
                    skewness = self._calculate_skewness(time_differences)
                    self._draw_chart(
                        fs_logger,
                        simple_chunk_times,
                        ctitle = "Parsed Chunk Times",
                    )
                    fs_logger.info(
                        "Parsed Chunk Rate: {chunk_generation_rate:.2f} Chunks/s",
                        chunk_generation_rate = chunk_generation_rate
                    )
                    fs_logger.info(
                        "Parsed First Chunk Wait Time: {chunk_wait_time:.2f}ms({format_time_duration})",
                        chunk_wait_time = first_chunk_wait_time / 1e6,
                        format_time_duration = format_time_duration_ns(first_chunk_wait_time, use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Parsed Chunk Average Time: {ave_chunk_spawn_time:.2f}ms({format_time_duration})",
                        ave_chunk_spawn_time = ave_chunk_spawn_time / 1e6,
                        format_time_duration = format_time_duration_ns(int(ave_chunk_spawn_time), use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Parsed Chunk Max Time: {max_chunk_spawn_time:.2f}ms({format_time_duration})",
                        max_chunk_spawn_time = max_chunk_spawn_time / 1e6,
                        format_time_duration = format_time_duration_ns(max_chunk_spawn_time, use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Parsed Chunk Min Time: {min_chunk_spawn_time:.2f}ms({format_time_duration})",
                        min_chunk_spawn_time = min_chunk_spawn_time / 1e6,
                        format_time_duration = format_time_duration_ns(min_chunk_spawn_time, use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Parsed Chunk Time CV: {chunk_stability_cv:.2%}",
                        chunk_stability_cv = chunk_stability_cv,
                    )
                    fs_logger.info(
                        "Parsed Chunk Time Range: {chunk_stability_range:.2f}ms({format_time_duration})",
                        chunk_stability_range = (max_chunk_spawn_time - min_chunk_spawn_time) / 1e6,
                        format_time_duration = format_time_duration_ns(max_chunk_spawn_time - min_chunk_spawn_time, use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Parsed Chunk Time Median: {chunk_median_time:.2f}ms({format_time_duration})",
                        chunk_median_time = chunk_median_time / 1e6,
                        format_time_duration = format_time_duration_ns(chunk_median_time, use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Parsed Chunk Time STD: {chunk_std_time:.2f}ms({format_time_duration})",
                        chunk_std_time = chunk_spawn_time_std / 1e6,
                        format_time_duration = format_time_duration_ns(int(chunk_spawn_time_std), use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Parsed Chunk Time MAD: {chunk_mad_time:.2f}ms({format_time_duration})",
                        chunk_mad_time = chunk_spawn_time_mad / 1e6,
                        format_time_duration = format_time_duration_ns(int(chunk_spawn_time_mad), use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Parsed Chunk Time Relative MAD: {chunk_relative_time_mad:.2%}",
                        chunk_relative_time_mad = chunk_spawn_time_relative_mad
                    )
                    fs_logger.info(
                        "Parsed Chunk Time IQR: {chunk_iqr_time:.2f}ms({format_time_duration})",
                        chunk_iqr_time = chunk_spawn_time_iqr / 1e6,
                        format_time_duration = format_time_duration_ns(int(chunk_spawn_time_iqr), use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Parsed Chunk Time IDR: {chunk_idr_time:.2f}ms({format_time_duration})",
                        chunk_idr_time = chunk_spawn_time_idr / 1e6,
                        format_time_duration = format_time_duration_ns(int(chunk_spawn_time_idr), use_abbreviation=True)
                    )
                    fs_logger.info(
                        "Parsed Chunk Time Skewness {chunk_time_skewness:.4f}",
                        chunk_time_skewness = skewness
                    )
                    fs_logger.info(
                        "Parsed Max Queue Backlog: {max_queue_backlog}",
                        max_queue_backlog = queue_backlog.max()
                    )
                    fs_logger.info(
                        "Parsed Min Queue Backlog: {min_queue_backlog}",
                        min_queue_backlog = queue_backlog.min()
                    )
                    fs_logger.info(
                        "Parsed Mean Queue Backlog: {mean_queue_backlog:.4f}",
                        mean_queue_backlog = queue_backlog.mean()
                    )
                    fs_logger.info(
                        "Parsed Median Queue Backlog: {median_queue_backlog:.4f}",
                        median_queue_backlog = np.median(queue_backlog)
                    )

        fs_logger.info("=========== Token Count ============")
        fs_logger.info(
            "Total Tokens: {total_tokens}({format_token_duration}Tokens)",
            total_tokens = response.token_usage.total_tokens,
            format_token_duration = format_token_duration(response.token_usage.total_tokens, use_abbreviation = True, delimiter = " ")
        )
        fs_logger.info(
            "Context Input Tokens: {prompt_tokens}({format_token_duration}Tokens)",
            prompt_tokens = response.token_usage.prompt_tokens,
            format_token_duration = format_token_duration(response.token_usage.prompt_tokens, use_abbreviation = True, delimiter = " ")
        )

        if response.token_usage.prompt_cache_hit_tokens is not None:
            fs_logger.info(
                "Cache Hit Count: {prompt_cache_hit_tokens}({format_token_duration}Tokens)",
                prompt_cache_hit_tokens = response.token_usage.prompt_cache_hit_tokens,
                format_token_duration = format_token_duration(response.token_usage.prompt_cache_hit_tokens, use_abbreviation = True, delimiter = " ")
            )
        if response.token_usage.prompt_cache_miss_tokens is not None:
            fs_logger.info(
                "Cache Miss Count: {prompt_cache_miss_tokens}({format_token_duration}Tokens)",
                prompt_cache_miss_tokens = response.token_usage.prompt_cache_miss_tokens,
                format_token_duration = format_token_duration(response.token_usage.prompt_cache_miss_tokens, use_abbreviation = True, delimiter = " ")
            )

        fs_logger.info(
            "Completion Output Tokens: {completion_tokens}({format_token_duration}Tokens)",
            completion_tokens = response.token_usage.completion_tokens,
            format_token_duration = format_token_duration(response.token_usage.completion_tokens, use_abbreviation = True, delimiter = " ")
        )
        
        if not math.isnan(response.token_usage.cache_hit_ratio()):
            fs_logger.info(
                "Cache Hit Ratio: {cache_hit_ratio:.2%}",
                cache_hit_ratio = response.token_usage.cache_hit_ratio()
            )
        if response.stream and response.request_log.chunk_times:
            if len(response.request_log.chunk_times) > 1:
                fs_logger.info(
                    "Average Generation Rate: {avg_gen_rate:.2f} Token/s",
                    avg_gen_rate = response.token_usage.completion_tokens / 
                    (
                        (
                            response.request_log.chunk_times[-1].monotonic -
                            response.request_log.chunk_times[0].monotonic
                        ) / 1e9
                    )
                )

        fs_logger.info("============= Content ==============")
        historical_context_text_length = response.historical_context.total_length
        new_context_text_length = response.new_context.total_length
        response.request_log.reasoning_content_length = sum(len(content.reasoning_content) for content in response.new_context.context_list if content.reasoning_content)
        response.request_log.new_content_length = sum(len(content.content) for content in response.new_context.context_list)

        fs_logger.info(
            "Total Content Length: {total_context_length}",
            total_context_length = historical_context_text_length + new_context_text_length
        )
        response.request_log.total_context_length = response.historical_context.total_length
        fs_logger.info(
            "New Reasoning Content Length: {reasoning_content_length}",
            reasoning_content_length = response.request_log.reasoning_content_length
        )
        fs_logger.info(
            "New Answer Content Length: {new_content_length}",
            new_content_length = response.request_log.new_content_length
        )
        fs_logger.info(
            "Historical Context Text Length: {historical_context_length}",
            historical_context_length = historical_context_text_length
        )
        fs_logger.info(
            "New Content Text Length: {new_context_length}",
            new_context_length = new_context_text_length
        )

        fs_logger.info("====================================")