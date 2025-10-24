import os
import sys

from .file import (
    stem,
    write_file,
    check_dir,
    check_dir_async,
    ensure_dir,
    read_dir_recur,
    move_directory_not_recur,
    listdir_recur,
    rmtree,
    move_file,
    copy_file,
    copy_file2,
    open_tar,
    utime,
)
from .time_range import divide_time_range

targets = [
    "file",
    "time_split",
]
if os.getenv("PY_ENV") != "prod":
    for name in list(sys.modules.keys()):
        for target in targets:
            if name.startswith(f"{__name__}.{target}"):
                sys.modules[name] = None  # type: ignore
