from .size_ratio_checker import SizeRatioChecker
from ..encoder import EncodingRequest


class EncodingQualityEstimator:
    def __init__(self, checker: SizeRatioChecker):
        self.__checker = checker

    async def estimate(
        self,
        req: EncodingRequest,
        quality_range: tuple[int, int],
        size_rate_range: tuple[float, float],
    ) -> int:
        quality_list = list(range(quality_range[0], quality_range[1] + 1))
        if not quality_list:
            raise ValueError("Invalid quality range")

        left, right = 0, len(quality_list) - 1
        best_quality = -1

        # 이진 탐색으로 적절한 quality 값 탐색
        while left <= right:
            mid = (left + right) // 2
            tgt_quality = quality_list[mid]

            size_ratio = await self.__checker.check(req, tgt_quality)

            if size_rate_range[0] <= size_ratio <= size_rate_range[1]:
                # 목표 범위에 맞는 quality 값을 찾음
                # 그러나 더 최적의 quality 값이 있을 수 있으므로 탐색을 계속
                best_quality = tgt_quality
                left = mid + 1  # 더 높은 쪽으로 탐색을 계속 진행
            elif size_ratio < size_rate_range[0]:
                # 용량 비율이 너무 낮음 (quality 값이 너무 낮음) -> quality 값을 높여야 함
                left = mid + 1
            else:  # size_rate > size_rate_range[1]
                # 용량 비율이 너무 높음 (quality 값이 너무 높음) -> quality 값을 낮춰야 함
                right = mid - 1

        if best_quality != -1:
            return best_quality

        raise ValueError("Quality estimation failed")
