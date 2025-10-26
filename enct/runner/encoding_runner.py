import uuid

from aiofiles import os as aios
from pyutils import log, get_ext, path_join

from .encoding_config import read_encoding_config
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
        self.conf = read_encoding_config(conf_path)
        self.src_dir_path = self.conf.src_dir_path
        self.out_dir_path = self.conf.out_dir_path
        self.tmp_dir_path = self.conf.tmp_dir_path
        self.notifier = create_notifier(env=env.env, conf=env.untf) if env.untf is not None else None
        self.encoder = VideoEncoderImpl()
        checker = SizeRatioCheckerImpl(encoder=self.encoder, tmp_dir_path=self.tmp_dir_path)
        self.estimator = EncodingQualityEstimator(checker=checker)

    async def run(self):
        if not await aios.path.exists(self.tmp_dir_path):
            await aios.makedirs(self.tmp_dir_path, exist_ok=True)

        for file_path in await listdir_recur(self.src_dir_path):
            await self.__encode_one(file_path)

        if self.notifier is not None:
            await self.notifier.notify(f"Encoding Completed: {self.src_dir_path}")
        log.info(f"Encoding Completed: {self.src_dir_path}")

    async def __encode_one(self, file_path: str):
        est = self.conf.estimate
        sub_path = file_path.replace(self.src_dir_path, "")
        file_stem = f"{stem(file_path)}_{str(uuid.uuid4())}"
        ext = get_ext(file_path)
        if ext is None:
            raise ValueError(f"File without extension: {file_path}")
        tmp_src_path = path_join(self.tmp_dir_path, f"{file_stem}_src.{ext}")
        await copy_file2(file_path, tmp_src_path)

        try:
            tmp_out_path = path_join(self.tmp_dir_path, f"{file_stem}_out.{ext}")

            req = EncodingRequest(
                src_file_path=tmp_src_path,
                out_file_path=tmp_out_path,
                opts=self.conf.encoding.model_copy(),
            )

            if est is not None and est.enabled:
                quality = await self.estimator.estimate(enc_req=req, est_req=est.estimate, ck_req=est.check)
                req.opts.video_quality = quality

            log.info("Starting encoding", req.to_log_attr())

            enc_ret = await self.encoder.encode(req, logging=False)
            if enc_ret.stderr is not None and len(enc_ret.stderr.matched) > 0:
                for line in enc_ret.stderr.matched:
                    log.debug("Filtered stderr line", {"line": line})
            log.info("Encoding completed", enc_ret.to_attr())

            await aios.remove(tmp_src_path)

            out_file_path = path_join(self.out_dir_path, sub_path)
            await check_dir_async(out_file_path)
            await move_file(tmp_out_path, out_file_path)
        except Exception as e:
            await aios.remove(tmp_src_path)
            if self.notifier is not None:
                await self.notifier.notify(f"Failed to encoding: {sub_path}, err={e}")
            raise
