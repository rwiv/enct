from pathlib import Path

from aiofiles import os as aios
import pytest
from pyutils import find_project_root, path_join

from enct.encoder import EncodingRequest, VideoEncoderImpl, VideoEncoder, VideoScale, AudioCodec, VideoCodec

src_file_path = path_join(find_project_root(), "dev", "test", "assets", "enc", "test.mp4")
out_file_path = path_join(find_project_root(), "dev", "tmp", "test.mp4")


@pytest.mark.skip
@pytest.mark.asyncio
async def test_video_encoder():
    encoder = VideoEncoderImpl()
    await aios.makedirs(Path(out_file_path).parent, exist_ok=True)
    req = EncodingRequest(
        srcFilePath=src_file_path,
        outFilePath=out_file_path,
        videoCodec=VideoCodec.H265,
        videoQuality=32,
        videoPreset="p4",
        videoScale=VideoScale(width=1280, height=720),
        videoFrame=30,
        audioCodec=AudioCodec.OPUS,
        audioBitrateKb=128,
        enableGpu=True,
    )
    # req = EncodingRequest(
    #     srcFilePath=src_file_path,
    #     outFilePath=out_file_path,
    #     videoCodec=VideoCodec.AV1,
    #     videoQuality=48,
    #     videoPreset="p4",
    #     videoScale=None,
    #     videoFrame=30,
    #     audioCodec=AudioCodec.COPY,
    #     audioBitrateKb=None,
    #     enableGpu=True,
    # )
    result = await encoder.encode(req)
    await aios.remove(out_file_path)
    print(result)
