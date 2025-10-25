import abc
from abc import abstractmethod

from pydantic import BaseModel

from .encoding_request import EncodingRequest
from ..ffmpeg import FilteredStderr


class EncodingResult(BaseModel):
    out_file_path: str
    quantizer_avg: float | None = None
    bitrate_avg: float | None = None
    speed_avg: float | None = None
    duration: float
    stderr: FilteredStderr | None = None
    size_ratio: float

    def to_attr(self):
        copied = self.model_copy()
        copied.stderr = None
        return copied.model_dump(mode="json", exclude_none=True)


class VideoEncoder(abc.ABC):
    @abstractmethod
    async def encode(self, req: EncodingRequest, logging: bool = False) -> EncodingResult:
        pass
