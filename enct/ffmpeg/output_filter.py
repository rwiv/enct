from pydantic import BaseModel


# fmt: off
FILTER_PREFIXES = [
    "Svt[info]",
    "Svt[warn]",
]
FILTER_KEYWORDS = [
    "Last message repeated",
    "error while decoding",

    "More than 1000 frames duplicated",
    "More than 10000 frames duplicated",
    "More than 100000 frames duplicated",

    "deprecated pixel format used, make sure you did set range correctly",

    "corrupt decoded frame",

    "cabac decode of qscale diff failed",

    "Invalid NAL unit size",
    "missing picture in access unit with size",
    "Error splitting the input into NAL units",

    "Decoding error: Invalid data found when processing input",

    "co located POCs unavailable",
    "mmco: unref short failure",

    "unspecified pixel format",
    "Consider increasing the value for the 'analyzeduration' (0) and 'probesize' (5000000) options",
]
# fmt: on


class FilteredStderr(BaseModel):
    matched: list[str]
    filtered: str


class FfmpegEncodingOutputFilter:
    def filtered_stderr(self, stderr: bytes) -> FilteredStderr | None:
        if len(stderr) == 0:
            return None

        lines = stderr.decode("utf-8").splitlines()
        stderr_matched = []
        for prefix in FILTER_PREFIXES:
            lines, matched = _filter_by_prefix(lines, prefix)
            stderr_matched.extend(matched)
        for keyword in FILTER_KEYWORDS:
            lines, matched = _filter_by_keyword(lines, keyword)
            stderr_matched.extend(matched)

        return FilteredStderr(matched=stderr_matched, filtered="\n".join(lines))


def _filter_by_prefix(lines: list[str], prefix: str) -> tuple[list[str], list[str]]:
    a = []
    b = []
    for line in lines:
        if not line.startswith(prefix):
            a.append(line)
        else:
            b.append(line)
    return a, b


def _filter_by_keyword(lines: list[str], keyword: str) -> tuple[list[str], list[str]]:
    a = []
    b = []
    for line in lines:
        if not line.find(keyword) >= 0:
            a.append(line)
        else:
            b.append(line)
    return a, b
