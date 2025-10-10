import pytest
from pyutils import load_dotenv, path_join, find_project_root

load_dotenv(path_join(find_project_root(), "dev", ".env-batch-dev"))

from enct.common import get_env
from enct.external.notifier import UntfNotifier


@pytest.mark.skip
@pytest.mark.asyncio
async def test_untf():
    env = get_env()
    notifier = UntfNotifier(env.untf)
    await notifier.notify("test")
