from decimal import Decimal


def divide_time_range(start: str, end: str, n: int) -> list[tuple[str, str]]:
    start_time = Decimal(start)
    end_time = Decimal(end)

    if start_time >= end_time:
        raise ValueError("Invalid time range. Start time must be less than end time.")

    if not isinstance(n, int) or n <= 0:
        raise ValueError("Invalid n value. Must be a positive integer.")

    total_duration = end_time - start_time
    interval = total_duration / Decimal(n)

    result_ranges = []
    current_start = start_time

    for i in range(n):
        current_end = current_start + interval
        if i == n - 1:
            current_end = end_time

        result_ranges.append((f"{current_start:.3f}", f"{current_end:.3f}"))
        current_start = current_end

    return result_ranges
