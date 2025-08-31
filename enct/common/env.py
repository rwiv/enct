import os

from pydantic import BaseModel, constr

from ..external.notifier import UntfConfig


class Env(BaseModel):
    env: constr(min_length=1)
    config_path: constr(min_length=1) | None = None
    untf: UntfConfig


def get_env() -> Env:
    env = os.getenv("PY_ENV")
    if env is None:
        env = "dev"

    return Env(
        env=env,
        config_path=os.getenv("CONFIG_PATH") or None,
        untf=read_untf_env(),
    )


def read_untf_env():
    return UntfConfig(
        endpoint=os.getenv("UNTF_ENDPOINT"),
        api_key=os.getenv("UNTF_API_KEY"),
        topic=os.getenv("UNTF_TOPIC"),
    )
