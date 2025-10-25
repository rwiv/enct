import uuid
from decimal import Decimal

from aiofiles import os as aios
from pyutils import path_join, get_ext

from .size_ratio_checker import SizeRatioChecker
from ..encoder import VideoEncoder, EncodingRequest, TimeRange
from ..ffmpeg import get_info
from ..utils import divide_time_range, divide_size_ratio


class SizeRatioCheckerImpl(SizeRatioChecker):
    def __init__(self, encoder: VideoEncoder, tmp_dir_path: str):
        self.__encoder = encoder
        self.__tmp_dir_path = tmp_dir_path

    async def check(self, req: EncodingRequest, quality: int) -> float:
        n_parts = 2
        enc_duration = "12"

        vid_info = (await get_info(req.src_file_path)).format
        ext = get_ext(req.src_file_path)
        if ext is None:
            raise ValueError(f"File without extension: {req.src_file_path}")

        ratio_sum = 0
        for start, _ in divide_time_range("0", vid_info.duration, n_parts):
            new_time_range = TimeRange(start=start, end=str(Decimal(start) + Decimal(enc_duration)))

            src_req = req.to_copy_req()
            src_req.out_file_path = path_join(self.__tmp_dir_path, f"{uuid.uuid4()}.{ext}")
            src_req.time_range = new_time_range
            await self.__encoder.encode(req=src_req, logging=False)

            out_req = req.model_copy()
            out_req.video_quality = quality
            out_req.out_file_path = path_join(self.__tmp_dir_path, f"{uuid.uuid4()}.{ext}")
            out_req.time_range = new_time_range
            await self.__encoder.encode(req=out_req, logging=False)

            size_ratio = await divide_size_ratio(out_req.out_file_path, src_req.out_file_path)
            ratio_sum += size_ratio

            await aios.remove(src_req.out_file_path)
            await aios.remove(out_req.out_file_path)

        return ratio_sum / n_parts
