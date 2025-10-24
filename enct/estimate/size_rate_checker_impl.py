from .size_rate_checker import SizeRateChecker
from ..utils import divide_time_range


## TODO: implement this
class SizeRateCheckerImpl(SizeRateChecker):
    def __init__(self):
        pass

    def check(self, file_path: str, quality: int) -> float:
        start_time = "53.2"
        end_time = "193.5"
        n_parts = 5
        time_ranges = divide_time_range(start_time, end_time, n_parts)
        return -1
