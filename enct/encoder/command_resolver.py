from .encoding_request import EncodingOptions, EncodingRequest, VideoCodec, AudioCodec


class FfmpegCommandResolver:
    def resolve(self, req: EncodingRequest) -> list[str]:
        opts = req.opts
        video_codec = _resolve_video_codec(opts)
        audio_codec = _resolve_audio_codec(opts)
        audio_bitrate = _resolve_audio_bitrate(opts)
        vf = _resolve_vf(opts)

        command = ["ffmpeg"]

        if opts.enable_gpu:
            command.extend(["-hwaccel", "nvdec", "-hwaccel_output_format", "cuda"])

        command.extend(["-i", req.src_file_path])

        if opts.time_range is not None:
            command.extend(["-ss", opts.time_range.start, "-to", opts.time_range.end])

        command.extend(["-c:v", video_codec])

        if opts.video_quality is not None:
            if opts.enable_gpu:
                command.extend(["-cq", str(opts.video_quality)])
            else:
                command.extend(["-crf", str(opts.video_quality)])
        if opts.video_preset:
            command.extend(["-preset", opts.video_preset])

        if opts.video_max_bitrate is not None and not opts.enable_gpu:
            if opts.video_codec == VideoCodec.AV1:
                command.extend(["-svtav1-params", f"mbr={opts.video_max_bitrate}"])
            elif opts.video_codec == VideoCodec.H265:
                command.extend(
                    ["-x265-params", f"vbv-maxrate={opts.video_max_bitrate}:vbv-bufsize={opts.video_max_bitrate}"]
                )

        if vf:
            command.extend(["-vf", vf])

        command.extend(["-c:a", audio_codec])
        if audio_bitrate:
            command.extend(["-b:a", audio_bitrate])

        command.extend(["-v", "warning", "-progress", "-", req.out_file_path])

        return command


def _resolve_video_codec(opts: EncodingOptions) -> str:
    if opts.enable_gpu:
        if opts.video_codec == VideoCodec.H265:
            return "hevc_nvenc"
        elif opts.video_codec == VideoCodec.AV1:
            return "av1_nvenc"
        else:
            raise ValueError(f"Unsupported GPU video codec: {opts.video_codec}")
    else:
        if opts.video_codec == VideoCodec.H265:
            return "libx265"
        elif opts.video_codec == VideoCodec.AV1:
            return "libsvtav1"
        elif opts.video_codec == VideoCodec.COPY:
            return "copy"
        else:
            raise ValueError(f"Unsupported video codec: {opts.video_codec}")


def _resolve_audio_codec(opts: EncodingOptions) -> str:
    if opts.audio_codec == AudioCodec.AAC:
        return "aac"
    elif opts.audio_codec == AudioCodec.OPUS:
        return "libopus"
    elif opts.audio_codec == AudioCodec.COPY:
        return "copy"
    else:
        raise ValueError(f"Unsupported audio codec: {opts.audio_codec}")


def _resolve_audio_bitrate(opts: EncodingOptions) -> str | None:
    if opts.audio_bitrate_kb is not None:
        return f"{opts.audio_bitrate_kb}k"
    return None


def _resolve_vf(opts: EncodingOptions) -> str | None:
    vf = []
    if opts.video_scale:
        if opts.enable_gpu:
            vf.append(f"scale_cuda={opts.video_scale.width}:{opts.video_scale.height}")
        else:
            vf.append(f"scale={opts.video_scale.width}:{opts.video_scale.height}")
    if opts.video_frame:
        vf.append(f"fps={opts.video_frame}")
    return ",".join(vf) if vf else None
