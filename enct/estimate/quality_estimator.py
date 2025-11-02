from enum import Enum

from pydantic import BaseModel, Field

from .size_ratio_checker import SizeRatioChecker, EstimationSampleOption
from ..encoder import EncodingRequest


class EstimatePriority(Enum):
    COMPRESSION = "compression"
    QUALITY = "quality"


class EstimationRequest(BaseModel):
    priority: EstimatePriority
    quality_range: tuple[int, int] = Field(alias="qualityRange")
    size_ratio_range: tuple[float, float] = Field(alias="sizeRatioRange")


class EncodingQualityEstimator:
    def __init__(self, checker: SizeRatioChecker):
        self.__checker = checker

    async def estimate(
        self,
        enc_req: EncodingRequest,
        est_req: EstimationRequest,
        smp_opt: EstimationSampleOption,
    ) -> int:
        quality_list = list(range(est_req.quality_range[0], est_req.quality_range[1] + 1))
        if not quality_list:
            raise ValueError("Invalid quality range")
        if est_req.size_ratio_range[0] > est_req.size_ratio_range[1]:
            raise ValueError("Invalid size ratio range")

        left, right = 0, len(quality_list) - 1
        tgt_quality = -1

        # 이진 탐색으로 적절한 quality 값 탐색
        while left <= right:
            mid = (left + right) // 2
            cur_quality = quality_list[mid]

            size_ratio = await self.__checker.check(enc_req, smp_opt, cur_quality)
            # print(f"quality: {cur_quality}, size_ratio: {size_ratio}")

            if est_req.size_ratio_range[0] <= size_ratio <= est_req.size_ratio_range[1]:
                # 목표 범위에 맞는 quality 값을 찾음
                # 그러나 더 최적의 quality 값이 있을 수 있으므로 탐색을 계속
                tgt_quality = cur_quality

                if est_req.priority == EstimatePriority.QUALITY:
                    right = mid - 1  # 더 낮은 쪽으로 탐색을 계속 진행
                elif est_req.priority == EstimatePriority.COMPRESSION:
                    left = mid + 1  # 더 높은 쪽으로 탐색을 계속 진행
                else:
                    raise ValueError("Invalid priority")
            elif size_ratio < est_req.size_ratio_range[0]:
                # 용량 비율이 너무 낮음 (quality 값이 너무 높음) -> quality 값을 낮춰야 함
                right = mid - 1
            else:  # size_rate > size_rate_range[1]
                # 용량 비율이 너무 높음 (quality 값이 너무 낮음) -> quality 값을 높여야 함
                left = mid + 1

        if tgt_quality != -1:
            return tgt_quality

        raise ValueError("Quality estimation failed")
