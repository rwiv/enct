from enct.encoder import EncodingOptions, VideoCodec, VideoScale, AudioCodec
from enct.runner import EncodingSuffixResolver

resolver = EncodingSuffixResolver()


def test_suffix_resolver():
    opts = new_opts(
        enabled_gpu=True,
        video_quality=34,
        video_preset="p4",
    )
    assert resolver.resolve(opts) == "[gpu-34-p4]"

    opts = new_opts(
        enabled_gpu=True,
        video_quality=34,
        video_preset="p4",
        video_frame=30,
    )
    assert resolver.resolve(opts) == "[gpu-34-p4-30fps]"

    opts = new_opts(
        enabled_gpu=False,
        video_quality=28,
        video_preset="5",
        video_frame=30,
        video_max_bitrate=3000,
    )
    assert resolver.resolve(opts) == "[cpu-28-5-3000k-30fps]"


def new_opts(
    enabled_gpu: bool,
    video_quality: int,
    video_preset: str,
    video_frame: int | None = None,
    video_max_bitrate: int | None = None,
) -> EncodingOptions:
    return EncodingOptions(
        videoCodec=VideoCodec.AV1,
        videoQuality=video_quality,
        videoPreset=video_preset,
        videoScale=VideoScale(width=1280, height=720),
        videoFrame=video_frame,
        videoMaxBitrate=video_max_bitrate,
        audioCodec=AudioCodec.COPY,
        audioBitrateKb=128,
        enableGpu=enabled_gpu,
    )
