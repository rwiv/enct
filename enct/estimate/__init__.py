import os
import sys

from .quality_estimator import EncodingQualityEstimator
from .size_ratio_checker import SizeRatioChecker, SizeRatioCheckerFake
from .size_ratio_checker_impl import SizeRatioCheckerImpl

targets = [
    "quality_estimator",
    "size_rate_checker",
]
if os.getenv("PY_ENV") != "prod":
    for name in list(sys.modules.keys()):
        for target in targets:
            if name.startswith(f"{__name__}.{target}"):
                sys.modules[name] = None  # type: ignore
