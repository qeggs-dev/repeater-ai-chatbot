import numpy as np
from .....request_log import TimeStamp
from ..assist import (
    calculate_interquartile_range,
    calculate_interdecile_range,
    calculate_mad,
    calculate_cv,
    calculate_skewness,
    calculate_kurtosis,
    calculate_entropy,
    sample
)

class ChunkSpawnTime:
    def __init__(
        self,
        stream_processing_start_time: TimeStamp,
        stream_processing_end_time: TimeStamp,
        total_chunks: int,
        first_chunk_spawn_time: int,
        time_differences: np.ndarray[tuple[int], np.dtype[np.int64]],
        non_zero_time_differences: np.ndarray[tuple[int], np.dtype[np.int64]],
    ):
        self.max_chunk_spawn_time = int(np.max(time_differences))
        self.min_chunk_spawn_time = int(np.min(non_zero_time_differences))
        self.chunk_spawn_time_range = int(self.max_chunk_spawn_time - self.min_chunk_spawn_time)
        self.ave_chunk_spawn_time = float(np.mean(time_differences))
        self.chunk_median_time = float(np.median(time_differences))
        self.chunk_spawn_time_std = float(np.std(time_differences))
        self.chunk_spawn_time_iqr = calculate_interquartile_range(time_differences)
        self.chunk_spawn_time_idr = calculate_interdecile_range(time_differences)
        self.chunk_spawn_time_p01 = int(np.percentile(time_differences, 1, method="nearest"))
        self.chunk_spawn_time_p50 = int(np.percentile(time_differences, 50, method="nearest"))
        self.chunk_spawn_time_p75 = int(np.percentile(time_differences, 75, method="nearest"))
        self.chunk_spawn_time_p90 = int(np.percentile(time_differences, 90, method="nearest"))
        self.chunk_spawn_time_p95 = int(np.percentile(time_differences, 95, method="nearest"))
        self.chunk_spawn_time_p99 = int(np.percentile(time_differences, 99, method="nearest"))
        self.chunk_spawn_time_mad = calculate_mad(time_differences)
        if self.chunk_median_time != 0:
            self.chunk_spawn_time_relative_mad = self.chunk_spawn_time_mad / self.chunk_median_time
        else:
            self.chunk_spawn_time_relative_mad = np.nan
        
        stream_processing_time = stream_processing_end_time.monotonic - stream_processing_start_time.monotonic
        if stream_processing_time != 0:
            self.chunk_generation_rate = total_chunks / (stream_processing_time / 1e9)
        else:
            self.chunk_generation_rate = np.nan
        
        self.chunk_stability_cv = calculate_cv(time_differences)
        self.simple_chunk_times = sample(time_differences, 34)
        self.first_chunk_wait_time = first_chunk_spawn_time - stream_processing_start_time.monotonic
        self.skewness = calculate_skewness(time_differences)
        self.kurtosis = calculate_kurtosis(time_differences)
        self.entropy = calculate_entropy(time_differences)