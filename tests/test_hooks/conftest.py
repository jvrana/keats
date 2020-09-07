import os
import shutil
from os.path import abspath
from os.path import dirname
from os.path import join

import pytest

from keats.hooks.keats_version_up import logger
from keats.hooks.utils import cmd_output

logger.setLevel("DEBUG")
here = dirname(abspath(__file__))


@pytest.fixture
def fixtures():
    return join(here, "fixtures")


@pytest.fixture
def temp_git_dir(tmpdir):
    git_dir = tmpdir.join("gits")
    cmd_output("git", "init", "--", str(git_dir))
    yield git_dir


@pytest.fixture
def temp_dir(temp_git_dir):
    shutil.copy(
        join(here, "fixtures", "pyproject.toml"), temp_git_dir.join("pyproject.toml"),
    )
    open(temp_git_dir.join(".fixture"), "w").write("a" * 10)
    os.mkdir(temp_git_dir.join("fakekeats"))
    temp_git_dir.join('fakekeats/__init__.py').write('')
    return temp_git_dir
