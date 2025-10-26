import os
import sys

from .encoding_config import EncodingConfig, EstimateConfig
from .encoding_runner import EncodingRunner

targets = [
    "encoding_executor",
]
if os.getenv("PY_ENV") != "prod":
    for name in list(sys.modules.keys()):
        for target in targets:
            if name.startswith(f"{__name__}.{target}"):
                sys.modules[name] = None  # type: ignore
