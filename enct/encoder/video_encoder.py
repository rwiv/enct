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
        return {
            "out_file_path": self.out_file_path,
            "quantizer_avg": f"{self.quantizer_avg:.3f}",
            "bitrate_avg": f"{self.bitrate_avg:.3f}",
            "speed_avg": f"{self.speed_avg:.3f}",
            "duration": f"{self.duration:.3f}",
            "size_ratio": f"{self.size_ratio:.3f}",
        }


class VideoEncoder(abc.ABC):
    @abstractmethod
    async def encode(self, req: EncodingRequest, logging: bool = False) -> EncodingResult:
        pass
