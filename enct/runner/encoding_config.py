from pathlib import Path

import yaml
from pydantic import BaseModel, constr, Field

from ..encoder import EncodingOptions
from ..estimate import EstimationSampleOption, EstimationRequest


class EstimationConfig(BaseModel):
    enabled: bool
    request: EstimationRequest
    sample_option: EstimationSampleOption = Field(alias="sampleOption")


class EncodingConfig(BaseModel):
    src_dir_path: constr(min_length=1) = Field(alias="srcDirPath")
    out_dir_path: constr(min_length=1) = Field(alias="outDirPath")
    tmp_dir_path: constr(min_length=1) = Field(alias="tmpDirPath")
    encoding: EncodingOptions
    estimation: EstimationConfig | None = None


def read_encoding_config(config_path: str) -> EncodingConfig:
    if not Path(config_path).exists():
        raise FileNotFoundError(f"File not found: {config_path}")
    with open(config_path, "r") as file:
        text = file.read()
    return EncodingConfig(**yaml.load(text, Loader=yaml.FullLoader))
