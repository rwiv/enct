import pytest

from enct.estimate import SizeRateCheckerFake, EncodingQualityEstimator

dfp = "dummy.mp4"  # dummy_file_path
failure_message = "Quality estimation failed"


def test_tc_success_01_finds_optimal_quality_in_the_middle():
    """
    TC-SUCCESS-01: 목표 범위에 여러 품질 값이 해당할 때 가장 높은 값을 반환하는지 테스트
    """
    # given: 품질 15, 16이 유효 범위에 속하지만, 16이 더 높은(최적) 품질 값임
    # fmt: off
    fake_checker = SizeRateCheckerFake(out={
        10: 0.1, 11: 0.15, 12: 0.2, 13: 0.3, 14: 0.35,
        15: 0.45,  # 유효
        16: 0.55,  # 유효 (최적)
        17: 0.65, 18: 0.7, 19: 0.8, 20: 0.9
    })
    # fmt: on
    estimator = EncodingQualityEstimator(checker=fake_checker)

    # when
    result_quality = estimator.estimate(dfp, (10, 20), (0.4, 0.6))

    # then
    assert result_quality == 16


def test_tc_edge_01_raises_error_when_all_rates_are_too_low():
    """
    TC-EDGE-01: 모든 품질 값의 결과(용량 비율)가 목표 범위보다 낮을 때 예외 발생 테스트
    """
    # given: 모든 품질에 대해 0.7 이하의 용량 비율을 반환. 목표는 0.8 이상.
    all_qualities = range(10, 21)
    fake_checker = SizeRateCheckerFake(out={q: 0.7 for q in all_qualities})
    estimator = EncodingQualityEstimator(checker=fake_checker)

    # when/then
    with pytest.raises(ValueError, match=failure_message):
        estimator.estimate(dfp, (10, 20), (0.8, 1.0))


def test_tc_edge_02_raises_error_when_all_rates_are_too_high():
    """
    TC-EDGE-02: 모든 품질 값의 결과(용량 비율)가 목표 범위보다 높을 때 예외 발생 테스트
    """
    # given: 모든 품질에 대해 0.5 이상의 용량 비율을 반환. 목표는 0.4 이하.
    all_qualities = range(10, 21)
    fake_checker = SizeRateCheckerFake(out={q: 0.5 for q in all_qualities})
    estimator = EncodingQualityEstimator(checker=fake_checker)

    # when/then
    with pytest.raises(ValueError, match=failure_message):
        estimator.estimate(dfp, (10, 20), (0.2, 0.4))


def test_tc_invalid_01_raises_error_for_inverted_quality_range():
    """
    TC-INVALID-01: 품질 범위가 거꾸로 (start > end) 지정되었을 때 예외 발생 테스트
    """
    # given
    fake_checker = SizeRateCheckerFake(out={})
    estimator = EncodingQualityEstimator(checker=fake_checker)

    # when/then
    with pytest.raises(ValueError, match="Invalid quality range"):
        estimator.estimate(dfp, (20, 10), (0.4, 0.6))


def test_tc_invalid_02_raises_error_for_inverted_size_rate_range():
    """
    TC-INVALID-02: 용량 비율 범위가 거꾸로 (start > end) 지정되었을 때 예외 발생 테스트
    """
    # given: check 함수의 반환값이 무엇이든 조건문을 통과할 수 없음
    all_qualities = range(10, 21)
    fake_checker = SizeRateCheckerFake(out={q: 0.5 for q in all_qualities})
    estimator = EncodingQualityEstimator(checker=fake_checker)

    # when/then
    with pytest.raises(ValueError, match=failure_message):
        estimator.estimate(dfp, (10, 20), (0.6, 0.4))
