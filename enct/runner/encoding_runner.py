import asyncio
import uuid

from aiofiles import os as aios
from pyutils import log, get_ext, path_join, dirpath

from .encoding_config import read_encoding_config
from .suffix_resolver import EncodingSuffixResolver
from ..common import Env
from ..encoder import VideoEncoderImpl, EncodingRequest
from ..estimate import EncodingQualityEstimator, SizeRatioCheckerImpl
from ..external.notifier import create_notifier
from ..utils import listdir_recur, move_file, copy_file2, check_dir_async, stem


class EncodingRunner:
    def __init__(self, env: Env):
        conf_path = env.config_path
        if conf_path is None:
            raise ValueError("encoding_config_path is required")
        self.__conf = read_encoding_config(conf_path)

        self.__notifier = create_notifier(env=env.env, conf=env.untf) if env.untf is not None else None
        self.__encoder = VideoEncoderImpl()
        checker = SizeRatioCheckerImpl(encoder=self.__encoder, tmp_dir_path=self.__conf.tmp_dir_path)
        self.__estimator = EncodingQualityEstimator(checker=checker)
        self.__suffix_resolver = EncodingSuffixResolver()

    async def run(self):
        if not await aios.path.exists(self.__conf.tmp_dir_path):
            await aios.makedirs(self.__conf.tmp_dir_path, exist_ok=True)

        for file_path in await listdir_recur(self.__conf.src_dir_path):
            await self.__encode_one(file_path)

        if self.__notifier is not None:
            await self.__notifier.notify(f"Encoding Completed: {self.__conf.src_dir_path}")
        log.info(f"Encoding Completed: {self.__conf.src_dir_path}")

    async def __encode_one(self, file_path: str):
        est = self.__conf.estimate

        sub_path = file_path.replace(self.__conf.src_dir_path, "")
        file_stem = stem(file_path)
        ext = get_ext(file_path)
        if ext is None:
            raise ValueError(f"File without extension: {file_path}")

        tmp_stem = f"{file_stem}_{str(uuid.uuid4())}"
        tmp_src_path = path_join(self.__conf.tmp_dir_path, f"{tmp_stem}_src.{ext}")
        tmp_out_path = path_join(self.__conf.tmp_dir_path, f"{tmp_stem}_out.{ext}")
        await copy_file2(file_path, tmp_src_path)

        try:
            req = EncodingRequest(
                src_file_path=tmp_src_path,
                out_file_path=tmp_out_path,
                opts=self.__conf.encoding.model_copy(),
            )

            if est is not None and est.enabled:
                quality = await self.__estimator.estimate(enc_req=req, est_req=est.estimate, ck_req=est.check)
                req.opts.video_quality = quality

            log.info("Starting encoding", req.to_log_attr())

            enc_ret = await self.__encoder.encode(req, logging=False)
            if enc_ret.stderr is not None and len(enc_ret.stderr.matched) > 0:
                for line in enc_ret.stderr.matched:
                    log.debug("Filtered stderr line", {"line": line})
            log.info("Encoding completed", enc_ret.to_attr())

            await aios.remove(tmp_src_path)

            sub_base_path = dirpath(sub_path)
            filename = f"{file_stem} {self.__suffix_resolver.resolve(req.opts, enc_ret.size_ratio)}.{ext}"
            out_file_path = path_join(self.__conf.out_dir_path, sub_base_path, filename)

            await check_dir_async(out_file_path)
            await move_file(tmp_out_path, out_file_path)
        except Exception as e:
            if self.__notifier is not None:
                await self.__notifier.notify(f"Failed to encoding: {sub_path}, err={e}")
            await asyncio.sleep(1)
            await aios.remove(tmp_src_path)
            raise
