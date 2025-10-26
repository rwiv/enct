from ..encoder import EncodingOptions


class EncodingSuffixResolver:
    def resolve(self, opts: EncodingOptions, delimiter: str = "-") -> str:
        result = "["

        result += "gpu" if opts.enable_gpu else "cpu"
        result += delimiter

        if opts.video_quality is not None:
            result += f"{opts.video_quality}"
            result += delimiter

        if opts.video_preset is not None:
            result += f"{opts.video_preset}"
            result += delimiter

        if opts.video_max_bitrate is not None:
            result += f"{opts.video_max_bitrate}k"
            result += delimiter

        if opts.video_frame is not None:
            result += f"{opts.video_frame}fps"
            result += delimiter

        result = result[: -len(delimiter)]
        result += "]"
        return result
