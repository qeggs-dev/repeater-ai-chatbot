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
        queue_backlogs: np.ndarray[tuple[int], np.dtype[np.int64]],
    ):
        self.max_queue_backlog = int(np.max(queue_backlogs))
        self.min_queue_backlog = int(np.min(queue_backlogs))
        self.queue_backlog_range = self.max_queue_backlog - self.min_queue_backlog
        self.avg_queue_backlog = int(np.mean(queue_backlogs))
        self.median_queue_backlog = float(np.median(queue_backlogs))
        self.queue_backlog_std = float(np.std(queue_backlogs))
        self.queue_backlog_iqr = calculate_interquartile_range(queue_backlogs)
        self.queue_backlog_idr = calculate_interdecile_range(queue_backlogs)
        self.queue_backlog_p01 = np.percentile(queue_backlogs, 1, method="nearest")
        self.queue_backlog_p50 = np.percentile(queue_backlogs, 50, method="nearest")
        self.queue_backlog_p75 = np.percentile(queue_backlogs, 75, method="nearest")
        self.queue_backlog_p90 = np.percentile(queue_backlogs, 90, method="nearest")
        self.queue_backlog_p95 = np.percentile(queue_backlogs, 95, method="nearest")
        self.queue_backlog_p99 = np.percentile(queue_backlogs, 99, method="nearest")
        self.queue_backlog_mad = calculate_mad(queue_backlogs)
        if self.median_queue_backlog != 0:
            self.queue_backlog_relative_mad = self.queue_backlog_mad / self.median_queue_backlog
        else:
            self.queue_backlog_relative_mad = np.nan
        self.queue_backlog_cv = calculate_cv(queue_backlogs)
        self.queue_backlog_skewness = calculate_skewness(queue_backlogs)
        self.queue_backlog_kurtosis = calculate_kurtosis(queue_backlogs)
        self.queue_backlog_entropy = calculate_entropy(queue_backlogs)