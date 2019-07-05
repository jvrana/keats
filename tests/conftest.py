from os.path import dirname, join, abspath
import shutil

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
    f2 = f.mkdir("testpackage")
    f2 = f.mkdir("tests")

    shutil.copy(fake_pyproject, join(f, "pyproject.toml"))
    return f


@pytest.fixture
def fake_keats(fake_project):
    return Keats(fake_project)
