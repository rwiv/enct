import pytest
from aiofiles import os as aios
from pyutils import path_join, find_project_root

from enct.encoder import EncodingRequest, VideoEncoderImpl, VideoCodec, AudioCodec
from enct.estimate import SizeRatioCheckerImpl

src_dir_path = path_join(find_project_root(), "dev", "test", "assets", "enc")
tmp_dir_path = path_join(find_project_root(), "dev", "tmp")


@pytest.mark.skip
@pytest.mark.asyncio
async def test_size_ratio_checker_impl():
    encoder = VideoEncoderImpl()
    checker = SizeRatioCheckerImpl(encoder=encoder, tmp_dir_path=tmp_dir_path)

    await aios.makedirs(tmp_dir_path, exist_ok=True)

    req = EncodingRequest(
        srcFilePath=path_join(src_dir_path, "test.mp4"),
        outFilePath=path_join(tmp_dir_path, "x"),
        videoCodec=VideoCodec.AV1,
        videoQuality=48,
        videoPreset="p4",
        videoScale=None,
        videoFrame=30,
        # videoFrame=None,
        audioCodec=AudioCodec.COPY,
        audioBitrateKb=None,
        enableGpu=True,
    )
    size_ratio = await checker.check(req, 48)
    print(size_ratio)
