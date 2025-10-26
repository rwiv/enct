import os
import sys

from .quality_estimator import EncodingQualityEstimator, EstimateRequest, EstimatePriority
from .size_ratio_checker import SizeRatioChecker, SizeRatioCheckerFake, SizeCheckRequest
from .size_ratio_checker_impl import SizeRatioCheckerImpl
from .time_range_utils import get_sub_time_range

targets = [
    "quality_estimator",
    "size_rate_checker",
]
if os.getenv("PY_ENV") != "prod":
    for name in list(sys.modules.keys()):
        for target in targets:
            if name.startswith(f"{__name__}.{target}"):
                sys.modules[name] = None  # type: ignore
