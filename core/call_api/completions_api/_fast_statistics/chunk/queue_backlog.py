import numpy as np
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

class QueueBacklog:
    def __init__(
        self,
        raw_queue_backlogs: list[int] | None,
    ):
        self.queue_backlog = np.array(raw_queue_backlogs, dtype=np.int64)
        self.max_queue_backlog = int(np.max(self.queue_backlog))
        self.min_queue_backlog = int(np.min(self.queue_backlog))
        self.queue_backlog_range = self.max_queue_backlog - self.min_queue_backlog
        self.avg_queue_backlog = int(np.mean(self.queue_backlog))
        self.median_queue_backlog = float(np.median(self.queue_backlog))
        self.queue_backlog_std = float(np.std(self.queue_backlog))
        self.queue_backlog_iqr = calculate_interquartile_range(self.queue_backlog)
        self.queue_backlog_idr = calculate_interdecile_range(self.queue_backlog)
        self.queue_backlog_p01 = np.percentile(self.queue_backlog, 1, method="nearest")
        self.queue_backlog_p50 = np.percentile(self.queue_backlog, 50, method="nearest")
        self.queue_backlog_p75 = np.percentile(self.queue_backlog, 75, method="nearest")
        self.queue_backlog_p90 = np.percentile(self.queue_backlog, 90, method="nearest")
        self.queue_backlog_p95 = np.percentile(self.queue_backlog, 95, method="nearest")
        self.queue_backlog_p99 = np.percentile(self.queue_backlog, 99, method="nearest")
        self.queue_backlog_mad = calculate_mad(self.queue_backlog)
        if self.median_queue_backlog != 0:
            self.queue_backlog_relative_mad = self.queue_backlog_mad / self.median_queue_backlog
        else:
            self.queue_backlog_relative_mad = np.nan
        self.queue_backlog_cv = calculate_cv(self.queue_backlog)
        self.simple_backlog = sample(self.queue_backlog, 34)
        self.queue_backlog_skewness = calculate_skewness(self.queue_backlog)
        self.queue_backlog_kurtosis = calculate_kurtosis(self.queue_backlog)
        self.queue_backlog_entropy = calculate_entropy(self.queue_backlog)