from decimal import Decimal

from ..encoder import TimeRange


def get_sub_time_range(start: str, end: str, enc_duration: str):
    tr = TimeRange(start=start, end=end)
    if Decimal(enc_duration) < tr.get_duration():
        tr = TimeRange(start=start, end=str(Decimal(start) + Decimal(enc_duration)))
    return tr
