import asyncio
import logging

from pyutils import log

from .common import get_env
from .runner import EncodingRunner


if __name__ == "__main__":
    log.set_level(logging.DEBUG)
    env = get_env()
    asyncio.run(EncodingRunner(env).run())
