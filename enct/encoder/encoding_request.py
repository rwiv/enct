from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class VideoCodec(Enum):
    H265 = "h265"
    AV1 = "av1"
    COPY = "copy"


class AudioCodec(Enum):
    AAC = "aac"
    OPUS = "opus"
    COPY = "copy"


class VideoScale(BaseModel):
    width: int
    height: int


class TimeRange(BaseModel):
    start: str
    end: str

    def get_duration(self) -> Decimal:
        return Decimal(self.end) - Decimal(self.start)


class EncodingOptions(BaseModel):
    video_codec: VideoCodec = Field(alias="videoCodec", default=VideoCodec.COPY)
    video_quality: int | None = Field(alias="videoQuality", default=None)
    video_preset: str | None = Field(alias="videoPreset", default=None)
    video_max_bitrate: int | None = Field(alias="videoMaxBitrate", default=None)
    video_scale: VideoScale | None = Field(alias="videoScale", default=None)
    video_frame: int | None = Field(alias="videoFrame", default=None)
    audio_codec: AudioCodec = Field(alias="audioCodec", default=AudioCodec.COPY)
    audio_bitrate_kb: int | None = Field(alias="audioBitrateKb", default=None)
    time_range: TimeRange | None = Field(alias="timeRange", default=None)
    enable_gpu: bool = Field(alias="enableGpu", default=False)

    def to_copy_opts(self) -> "EncodingOptions":
        copied = self.model_copy()
        copied.video_codec = VideoCodec.COPY
        copied.video_quality = None
        copied.video_preset = None
        copied.video_max_bitrate = None
        copied.video_scale = None
        copied.video_frame = None
        copied.audio_codec = AudioCodec.COPY
        copied.audio_bitrate_kb = None
        copied.enable_gpu = False
        return copied


class EncodingRequest(BaseModel):
    src_file_path: str
    out_file_path: str
    opts: EncodingOptions

    def to_log_attr(self):
        return {
            "enable_gpu": self.opts.enable_gpu,
            "codec": self.opts.video_codec.value,
            "quality": self.opts.video_quality,
            "preset": self.opts.video_preset,
            "frame": self.opts.video_frame,
            "max_bitrate": self.opts.video_max_bitrate,
            "src_file": self.src_file_path,
        }

    def to_copy_req(self) -> "EncodingRequest":
        return EncodingRequest(
            src_file_path=self.src_file_path,
            out_file_path=self.out_file_path,
            opts=self.opts.to_copy_opts(),
        )
