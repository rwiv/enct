from pathlib import Path

from aiofiles import os as aios
import pytest
from pyutils import find_project_root, path_join

from enct.encoder import EncodingRequest, VideoEncoderImpl, VideoEncoder, VideoScale, AudioCodec, VideoCodec, EncodingOptions

src_file_path = path_join(find_project_root(), "dev", "test", "assets", "enc", "test.mp4")
out_file_path = path_join(find_project_root(), "dev", "tmp", "test.mp4")


@pytest.mark.skip
@pytest.mark.asyncio
async def test_video_encoder():
    encoder = VideoEncoderImpl()
    await aios.makedirs(Path(out_file_path).parent, exist_ok=True)
    opts = EncodingOptions(
        videoCodec=VideoCodec.H265,
        videoQuality=32,
        videoPreset="p4",
        videoScale=VideoScale(width=1280, height=720),
        videoFrame=30,
        audioCodec=AudioCodec.OPUS,
        audioBitrateKb=128,
        enableGpu=True,
    )
    # opts = EncodingOptions(
    #     enableGpu=True,
    #     videoCodec=VideoCodec.AV1,
    #     videoQuality=48,
    #     videoPreset="p4",
    #     videoScale=None,
    #     videoFrame=30,
    #     audioCodec=AudioCodec.COPY,
    #     audioBitrateKb=None,
    # )
    result = await encoder.encode(EncodingRequest(src_file_path=src_file_path, out_file_path=out_file_path, opts=opts))
    await aios.remove(out_file_path)
    print(result)
