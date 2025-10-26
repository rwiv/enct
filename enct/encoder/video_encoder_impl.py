import asyncio
import subprocess
import sys

from aiofiles import os as aios
from pyutils import log, exec_process, cur_duration, check_returncode

from .command_resolver import FfmpegCommandResolver
from .encoding_request import EncodingRequest
from .video_encoder import EncodingResult, VideoEncoder
from ..ffmpeg import FfmpegEncodingOutputFilter, FfmpegEncodingProgressParser
from ..utils import divide_size_ratio

WAIT_TIMEOUT_SEC = 1.0


class VideoEncoderImpl(VideoEncoder):
    def __init__(self):
        self.__out_filter = FfmpegEncodingOutputFilter()
        self.__cmd_resolver = FfmpegCommandResolver()
        self.__parser = FfmpegEncodingProgressParser()

    async def encode(self, req: EncodingRequest, logging: bool = False) -> EncodingResult:
        if await aios.path.exists(req.out_file_path):
            raise FileExistsError(f"Output file {req.out_file_path} already exists.")

        start_time = asyncio.get_event_loop().time()

        command = self.__cmd_resolver.resolve(req)
        process = await exec_process(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert process.stdout is not None

        stream_q_sum = 0.0
        stream_q_cnt = 0
        bitrate_sum = 0.0
        bitrate_cnt = 0
        speed_sum = 0.0
        speed_cnt = 0

        while True:
            chunk = await asyncio.wait_for(process.stdout.read(sys.maxsize), WAIT_TIMEOUT_SEC)
            if not chunk:
                break
            info = self.__parser.parse(chunk)
            if info.stream_q is not None:
                stream_q_sum += info.stream_q
                stream_q_cnt += 1
            if info.bitrate_kbits is not None:
                bitrate_sum += info.bitrate_kbits
                bitrate_cnt += 1
            if info.speed is not None:
                speed_sum += info.speed
                speed_cnt += 1
            if logging:
                log.debug("Encoding Progress", info.model_dump(mode="json"))

        stdout_raw, stderr_raw = await process.communicate()
        check_returncode(process, command, stdout_raw, stderr_raw)

        stderr = self.__out_filter.filtered_stderr(stderr_raw)
        if stderr is not None and len(stderr.filtered) > 0:
            await aios.remove(req.out_file_path)
            log.error("Encoding failed with error", {"err": stderr.filtered})
            raise RuntimeError("Encoding failed with error")

        return EncodingResult(
            out_file_path=req.out_file_path,
            quantizer_avg=stream_q_sum / stream_q_cnt if stream_q_cnt > 0 else None,
            bitrate_avg=bitrate_sum / bitrate_cnt if bitrate_cnt > 0 else None,
            speed_avg=speed_sum / speed_cnt if speed_cnt > 0 else None,
            duration=cur_duration(start_time),
            stderr=stderr,
            size_ratio=await divide_size_ratio(req.out_file_path, req.src_file_path),
        )
