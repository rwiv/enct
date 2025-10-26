import pytest

from enct.encoder import EncodingRequest, EncodingOptions
from enct.estimate import SizeRatioCheckerFake, EncodingQualityEstimator, SizeCheckRequest, EstimateRequest, EstimatePriority

enc_req = EncodingRequest(src_file_path="dummy.mp4", out_file_path="out.mp4", opts=EncodingOptions())
ck_req = SizeCheckRequest(nParts=2, encDuration="12")

comp = EstimatePriority.COMPRESSION
quality = EstimatePriority.QUALITY

fake_checker = SizeRatioCheckerFake()
estimator = EncodingQualityEstimator(checker=fake_checker)


# --- 1. 성공 케이스 (Success Cases) ---


@pytest.mark.asyncio
async def test_returns_valid_quality():
    """
    유효한 값 중 priority에 맞는 quality 값을 반환하는지 테스트
    """
    # given
    q_range = (10, 20)
    sr_range = (0.9, 1.1)
    # fmt: off
    fake_checker.set_out_map({
        10: 1.5, 11: 1.3, 12: 1.2,
        13: 1.1,  # 유효 (경계값)
        14: 1.0,  # 유효
        15: 0.9,  # 유효 (경계값)
        16: 0.8, 17: 0.7, 18: 0.6, 19: 0.5, 20: 0.4,
    })
    # fmt: on

    # when/then
    result_quality = await estimator.estimate(enc_req, est(comp, q_range, sr_range), ck_req)
    assert result_quality == 15

    # when/then
    result_quality = await estimator.estimate(enc_req, est(quality, q_range, sr_range), ck_req)
    assert result_quality == 13


@pytest.mark.asyncio
async def test_finds_single_valid_quality():
    """
    단 하나의 quality 값만 목표 범위에 맞는 경우 해당 값을 정확히 반환하는지 테스트
    """
    # given
    q_range = (20, 30)
    sr_range = (0.95, 1.05)
    out_map = {q: 1.5 for q in range(20, 31)}
    out_map[25] = 1.0  # 유일한 유효 값
    fake_checker.set_out_map(out_map)

    # when/then (어떤 우선순위든 동일한 결과를 반환해야 함)
    result_for_compression = await estimator.estimate(enc_req, est(comp, q_range, sr_range), ck_req)
    assert result_for_compression == 25

    result_for_quality = await estimator.estimate(enc_req, est(quality, q_range, sr_range), ck_req)
    assert result_for_quality == 25


@pytest.mark.asyncio
async def test_finds_optimal_quality_at_boundaries():
    """
    탐색 범위의 경계값이 최적의 quality 값인 경우를 테스트
    """
    # given: 상한 경계값이 정답인 경우 (압축률 우선)
    q_range = (20, 30)
    sr_range = (0.8, 1.2)
    out_map_upper = {q: 1.3 for q in range(20, 31)}
    out_map_upper[30] = 0.9  # 상한 경계값만 유효
    fake_checker.set_out_map(out_map_upper)

    # when
    result_upper = await estimator.estimate(enc_req, est(comp, q_range, sr_range), ck_req)

    # then
    assert result_upper == 30

    # given: 하한 경계값이 정답인 경우 (품질 우선)
    out_map_lower = {q: 0.7 for q in range(20, 31)}
    out_map_lower[20] = 1.1  # 하한 경계값만 유효
    fake_checker.set_out_map(out_map_lower)

    # when
    result_lower = await estimator.estimate(enc_req, est(quality, q_range, sr_range), ck_req)

    # then
    assert result_lower == 20


# --- 2. 실패 및 예외 케이스 (Failure & Exception Cases) ---


@pytest.mark.asyncio
async def test_raises_error_when_no_valid_quality_found():
    """
    유효한 quality 값을 하나도 찾지 못할 때 ValueError를 발생시키는지 테스트
    """
    # given
    q_range = (1, 10)
    sr_range = (0.9, 1.1)
    # 항상 범위를 벗어나는 값만 반환
    fake_checker.set_out_map({q: 1.5 for q in range(1, 11)})

    # when/then
    with pytest.raises(ValueError, match="Quality estimation failed"):
        await estimator.estimate(enc_req, est(comp, q_range, sr_range), ck_req)


@pytest.mark.asyncio
async def test_raises_error_for_invalid_quality_range():
    """
    quality, size_ratio 탐색 범위가 유효하지 않을 때 ValueError를 발생시키는지 테스트
    """
    # given
    fake_checker.set_out_map({})  # checker는 호출되지 않음

    # when/then
    with pytest.raises(ValueError, match="Invalid quality range"):
        await estimator.estimate(enc_req, est(comp, (30, 20), (0.9, 1.1)), ck_req)
    with pytest.raises(ValueError, match="Invalid size ratio range"):
        await estimator.estimate(enc_req, est(comp, (20, 30), (1.1, 0.9)), ck_req)


def est(priority: EstimatePriority, quality_range: tuple[int, int], size_ratio_range: tuple[float, float]):
    return EstimateRequest(priority=priority, qualityRange=quality_range, sizeRatioRange=size_ratio_range)
