import uuid

from aiofiles import os as aios
from pyutils import path_join, get_ext

from .size_ratio_checker import SizeRatioChecker, SizeCheckRequest
from .time_range_utils import get_sub_time_range
from ..encoder import VideoEncoder, EncodingRequest
from ..ffmpeg import get_info
from ..utils import divide_time_range, divide_size_ratio


class SizeRatioCheckerImpl(SizeRatioChecker):
    def __init__(self, encoder: VideoEncoder, tmp_dir_path: str):
        self.__encoder = encoder
        self.__tmp_dir_path = tmp_dir_path

    async def check(self, enc_req: EncodingRequest, ck_req: SizeCheckRequest, quality: int) -> float:
        vid_info = (await get_info(enc_req.src_file_path)).format
        ext = get_ext(enc_req.src_file_path)
        if ext is None:
            raise ValueError(f"File without extension: {enc_req.src_file_path}")

        ratio_sum = 0
        for i, (start, end) in enumerate(divide_time_range("0", vid_info.duration, ck_req.n_parts + 1)):
            if i == 0:
                continue

            src_req = enc_req.to_copy_req()
            src_req.out_file_path = path_join(self.__tmp_dir_path, f"{uuid.uuid4()}.{ext}")
            src_req.opts.time_range = get_sub_time_range(start, end, ck_req.enc_duration)
            await self.__encoder.encode(req=src_req, logging=False)

            out_req = enc_req.model_copy(deep=True)
            out_req.src_file_path = src_req.out_file_path
            out_req.out_file_path = path_join(self.__tmp_dir_path, f"{uuid.uuid4()}.{ext}")
            out_req.opts.video_quality = quality
            out_req.opts.time_range = None
            await self.__encoder.encode(req=out_req, logging=False)

            size_ratio = await divide_size_ratio(out_req.out_file_path, src_req.out_file_path)
            ratio_sum += size_ratio

            await aios.remove(src_req.out_file_path)
            await aios.remove(out_req.out_file_path)

        return ratio_sum / ck_req.n_parts
