import pytest
from decimal import InvalidOperation

from enct.utils import divide_time_range


# 1. 성공 케이스 (Happy Path)
# fmt: off
@pytest.mark.parametrize("start, end, n, expected", [
    # 테스트 1.1: 기본적인 경우 (정수로 나누어 떨어짐)
    ("0.000", "10.000", 5,
     [("0.000", "2.000"), ("2.000", "4.000"), ("4.000", "6.000"), ("6.000", "8.000"), ("8.000", "10.000")]),

    # 테스트 1.2: 나누어 떨어지지 않는 경우 (소수점 발생)
    ("0.000", "1.000", 3, [("0.000", "0.333"), ("0.333", "0.667"), ("0.667", "1.000")]),

    # 테스트 1.3: n이 1인 경우
    ("5.000", "10.000", 1, [("5.000", "10.000")]),

    # 테스트 1.4: 복잡한 소수점을 가진 시간 범위
    # Decimal 타입 덕분에 부동소수점 오류 없이 정확한 계산이 가능합니다.
    ("1.234", "5.678", 4, [("1.234", "2.345"), ("2.345", "3.456"), ("3.456", "4.567"), ("4.567", "5.678")]),
])
# fmt: on
def test_divide_time_range_success_cases(start, end, n, expected):
    """함수가 정상적인 입력에 대해 올바른 시간 구간 리스트를 반환하는지 테스트합니다."""
    assert divide_time_range(start, end, n) == expected


# 2. 엣지 케이스 (Edge Cases)
def test_divide_time_range_with_large_n():
    """매우 큰 n 값에 대해서도 함수가 올바르게 동작하는지 테스트합니다."""
    start, end, n = "0.000", "1.000", 1000
    result = divide_time_range(start, end, n)

    assert len(result) == n
    assert result[0][0] == start
    assert result[-1][1] == end  # 마지막 구간의 끝은 항상 end 값과 일치해야 합니다.
    assert result[0] == ("0.000", "0.001")


def test_divide_time_range_with_small_interval():
    """매우 작은 시간 간격에 대해서도 정밀도를 유지하며 올바르게 계산하는지 테스트합니다."""
    start, end, n = "0.000", "0.001", 2
    expected = [("0.000", "0.000"), ("0.000", "0.001")]

    assert divide_time_range(start, end, n) == expected


# 3. 오류 처리 케이스 (Error Handling)
# fmt: off
@pytest.mark.parametrize("start, end", [
    ("10.000", "0.000"),  # 시작 시간이 종료 시간보다 큰 경우
    ("5.000", "5.000"),  # 시작 시간과 종료 시간이 같은 경우
])
# fmt: on
def test_invalid_time_range_raises_value_error(start, end):
    """잘못된 시간 범위(start >= end)가 주어졌을 때 ValueError가 발생하는지 테스트합니다."""
    with pytest.raises(ValueError, match="Invalid time range"):
        divide_time_range(start, end, n=5)


# fmt: off
@pytest.mark.parametrize("n", [
    0,  # n이 0인 경우
    -1,  # n이 음수인 경우
    2.5,  # n이 정수가 아닌 경우
])
# fmt: on
def test_invalid_n_value_raises_value_error(n):
    """n이 양의 정수가 아닐 때 ValueError가 발생하는지 테스트합니다."""
    with pytest.raises(ValueError, match="Invalid n value"):
        divide_time_range("0.000", "10.000", n)


# fmt: off
@pytest.mark.parametrize("start, end", [
    ("abc", "10.000"),  # start가 숫자가 아닌 경우
    ("0.000", "xyz"),  # end가 숫자가 아닌 경우
])
# fmt: on
def test_non_numeric_time_string_raises_error(start, end):
    """시간 문자열이 숫자로 변환될 수 없을 때 InvalidOperation 예외가 발생하는지 테스트합니다."""
    with pytest.raises(InvalidOperation):
        divide_time_range(start, end, n=5)
