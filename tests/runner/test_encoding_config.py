from enct.encoder import EncodingOptions
from enct.estimate import EstimationSampleOption, EstimationRequest, EstimatePriority
from enct.runner import EncodingConfig, EstimationConfig


def test_encoding_config():
    est = EstimationConfig(
        enabled=False,
        request=EstimationRequest(
            priority=EstimatePriority.QUALITY,
            qualityRange=(1, 2),
            sizeRatioRange=(1, 2),
        ),
        sampleOption=EstimationSampleOption(size=3, duration="10"),
    )
    EncodingConfig(
        srcDirPath="a",
        outDirPath="b",
        tmpDirPath="c",
        encoding=EncodingOptions(),
        estimation=est,
    )
