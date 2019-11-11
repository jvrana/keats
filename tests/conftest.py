import shutil
from os.path import abspath
from os.path import dirname
from os.path import join

import pytest

from keats import Keats

here = join(abspath(dirname(__file__)))
data = join(here, "data")


@pytest.fixture(scope="module")
def fake_pyproject():
    return join(data, "fake_pyproject.toml")


@pytest.fixture
def fake_project(fake_pyproject, tmpdir):
    f = tmpdir.mkdir("testpackage")
    f.mkdir("testpackage")
    f.mkdir("tests")

    shutil.copy(fake_pyproject, join(str(f), "pyproject.toml"))
    return f


@pytest.fixture
def fake_keats(fake_project):
    return Keats(fake_project)
