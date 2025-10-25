import abc
from abc import abstractmethod

from ..encoder import EncodingRequest


class SizeRatioChecker(abc.ABC):
    @abstractmethod
    async def check(self, req: EncodingRequest, quality: int) -> float:
        """
        :param req: video encoding request
        :param quality: video encoding quality
        :return: estimated video size ratio
        """
        pass


class SizeRatioCheckerFake(SizeRatioChecker):
    def __init__(self, out: dict[int, float]):
        self.__out = out

    async def check(self, req: EncodingRequest, quality: int) -> float:
        return self.__out[quality]
