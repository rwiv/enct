import abc
from abc import abstractmethod


class SizeRateChecker(abc.ABC):
    @abstractmethod
    def check(self, file_path: str, quality: int) -> float:
        """
        :param file_path: input video file path
        :param quality: video encoding quality
        :return: estimated video size ratio
        """
        pass


class SizeRateCheckerFake(SizeRateChecker):
    def __init__(self, out: dict[int, float]):
        self.__out = out

    def check(self, file_path: str, quality: int) -> float:
        return self.__out[quality]
