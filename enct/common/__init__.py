import os
import sys

from .env import Env, get_env

targets = [
    "env_batch",
    "env_celery",
    "env_common_configs",
    "env_configs",
    "env_server",
    "env_worker",
]
if os.getenv("PY_ENV") != "prod":
    for name in list(sys.modules.keys()):
        for target in targets:
            if name.startswith(f"{__name__}.{target}"):
                sys.modules[name] = None  # type: ignore
