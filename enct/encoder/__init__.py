import os
import sys

from .command_resolver import FfmpegCommandResolver
from .encoding_request import EncodingRequest, VideoCodec, VideoScale, AudioCodec, TimeRange
from .video_encoder import VideoEncoder
from .video_encoder_impl import VideoEncoderImpl

targets = [
    "command_resolver",
    "encoding_request",
    "output_filter",
    "progress_parser",
    "video_encoder",
    "video_encoder_impl",
]
if os.getenv("PY_ENV") != "prod":
    for name in list(sys.modules.keys()):
        for target in targets:
            if name.startswith(f"{__name__}.{target}"):
                sys.modules[name] = None  # type: ignore
