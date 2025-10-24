from .size_rate_checker import SizeRateChecker


class EncodingQualityEstimator:
    def __init__(self, checker: SizeRateChecker):
        self.__checker = checker

    def estimate(
        self,
        file_path: str,
        quality_range: tuple[int, int],
        size_rate_range: tuple[float, float],
    ) -> int:
        quality_list = list(range(quality_range[0], quality_range[1] + 1))
        if not quality_list:
            raise ValueError("Invalid quality range")

        left, right = 0, len(quality_list) - 1
        best_quality = -1

        while left <= right:
            mid = (left + right) // 2
            tgt_quality = quality_list[mid]

            size_ratio = self.__checker.check(file_path, tgt_quality)

            if size_rate_range[0] <= size_ratio <= size_rate_range[1]:
                # 목표 범위에 맞는 품질을 찾음
                # 그러나 더 적절한 품질(더 높은 품질)이 있을 수 있으므로 탐색을 계속
                best_quality = tgt_quality
                left = mid + 1  # 더 높은 품질 쪽으로 탐색을 계속 진행
            elif size_ratio < size_rate_range[0]:
                # 용량 비율이 너무 낮음 (품질이 너무 낮음) -> 품질을 높여야 함
                left = mid + 1
            else:  # size_rate > size_rate_range[1]
                # 용량 비율이 너무 높음 (품질이 너무 높음) -> 품질을 낮춰야 함
                right = mid - 1

        if best_quality != -1:
            return best_quality

        raise ValueError("Quality estimation failed")
