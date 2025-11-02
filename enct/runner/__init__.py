import os
import sys

from .encoding_config import EncodingConfig, EstimationConfig
from .encoding_runner import EncodingRunner
from .suffix_resolver import EncodingSuffixResolver

targets = ["encoding_config", "encoding_runner", "suffix_resolver"]
if os.getenv("PY_ENV") != "prod":
    for name in list(sys.modules.keys()):
        for target in targets:
            if name.startswith(f"{__name__}.{target}"):
                sys.modules[name] = None  # type: ignore
