import pytest
from aiofiles import os as aios
from pyutils import path_join, find_project_root

from enct.encoder import EncodingRequest, VideoEncoderImpl, VideoCodec, AudioCodec, EncodingOptions
from enct.estimate import SizeRatioCheckerImpl, SizeCheckRequest

src_dir_path = path_join(find_project_root(), "dev", "test", "assets", "enc")
tmp_dir_path = path_join(find_project_root(), "dev", "tmp")


@pytest.mark.skip
@pytest.mark.asyncio
async def test_size_ratio_checker_impl():
    encoder = VideoEncoderImpl()
    checker = SizeRatioCheckerImpl(encoder=encoder, tmp_dir_path=tmp_dir_path)

    await aios.makedirs(tmp_dir_path, exist_ok=True)

    opts = EncodingOptions(
        enableGpu=True,
        videoCodec=VideoCodec.AV1,
        videoQuality=48,
        videoPreset="p4",
        videoScale=None,
        videoFrame=30,
        # videoFrame=None,
        audioCodec=AudioCodec.COPY,
        audioBitrateKb=None,
    )
    enc_req = EncodingRequest(
        src_file_path=path_join(src_dir_path, "test.mp4"),
        out_file_path=path_join(tmp_dir_path, "x"),
        opts=opts,
    )
    c_req = SizeCheckRequest(nParts=2, encDuration="12")
    size_ratio = await checker.check(enc_req, c_req, 48)
    print(size_ratio)
