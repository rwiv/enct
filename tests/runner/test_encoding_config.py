from enct.encoder import EncodingOptions
from enct.estimate import SizeCheckRequest, EstimateRequest, EstimatePriority
from enct.runner import EncodingConfig, EstimateConfig


def test_encoding_config():
    est = EstimateConfig(
        enabled=False,
        estimate=EstimateRequest(
            priority=EstimatePriority.QUALITY,
            qualityRange=(1, 2),
            sizeRatioRange=(1, 2),
        ),
        check=SizeCheckRequest(nParts=3, encDuration="10"),
    )
    EncodingConfig(
        srcDirPath="a",
        outDirPath="b",
        tmpDirPath="c",
        encoding=EncodingOptions(),
        estimate=est,
    )
