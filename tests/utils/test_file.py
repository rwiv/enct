from aiofiles import os as aios
import pytest
from pyutils import path_join, find_project_root

from enct.utils import divide_file_size, write_file

tmp_dir_path = path_join(find_project_root(), "dev", "tmp")


@pytest.mark.skip
@pytest.mark.asyncio
async def test_divide_size_ratio():
    a_path = path_join(tmp_dir_path, "a.txt")
    b_path = path_join(tmp_dir_path, "b.txt")

    await write_file(a_path, "aa")
    await write_file(b_path, "aaaaaaaa")
    size_ratio = await divide_file_size(a_path, b_path)

    await aios.remove(a_path)
    await aios.remove(b_path)

    assert f"{size_ratio:.3f}" == "0.250"
