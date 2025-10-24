import os
import sys

from .ffprobe import get_info
from .output_filter import FfmpegEncodingOutputFilter, FilteredStderr
from .progress_parser import ProgressInfo, FfmpegEncodingProgressParser

targets = [
    "ffprobe_stream" "output_filter",
    "progress_parser",
]
if os.getenv("PY_ENV") != "prod":
    for name in list(sys.modules.keys()):
        for target in targets:
            if name.startswith(f"{__name__}.{target}"):
                sys.modules[name] = None  # type: ignore
