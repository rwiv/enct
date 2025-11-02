import abc
from abc import abstractmethod

from pydantic import BaseModel, field_validator, Field

from ..encoder import EncodingRequest


class EstimationSampleOption(BaseModel):
    size: int
    duration: str

    @field_validator("duration")
    @classmethod
    def check_integer_string(cls, v: str) -> str:
        try:
            float(v)
        except ValueError:
            raise ValueError(f"'{v}' is not a valid integer string")
        return v


class SizeRatioChecker(abc.ABC):
    @abstractmethod
    async def check(self, enc_req: EncodingRequest, ck_req: EstimationSampleOption, quality: int) -> float:
        """
        :param enc_req: video encoding request
        :param ck_req: size check request
        :param quality: video encoding quality
        :return: estimated video size ratio
        """
        pass


class SizeRatioCheckerFake(SizeRatioChecker):
    def __init__(self):
        self.__out = {}

    async def check(self, enc_req: EncodingRequest, ck_req: EstimationSampleOption, quality: int) -> float:
        return self.__out[quality]

    def set_out_map(self, out: dict[int, float]):
        self.__out = out
