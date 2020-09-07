from os.path import abspath
from os.path import dirname
from os.path import isfile
from os.path import join

import pytest

from keats import Keats


here = join(abspath(dirname(__file__)))
data = join(here, "fixtures")


def test_version(fake_keats):
    """We expect the version to be correctly returned."""
    assert fake_keats.v() == "9.9.9"


def test_package(fake_keats):
    """We expect the package name to be correctly returned."""
    assert fake_keats.package() == "testpackage"


def test_name(fake_keats):
    """We expect the package name to be correctly returned."""
    assert fake_keats.name() == "mypkg"


def test_format(fake_keats):
    """We expect a successfully implemented format."""
    fake_keats.run.format()


def test_version_json(fake_keats):
    """We expect the package info to be written to a version.py file.

    We then check the contents of that file with 'exec' and verify its
    contents with the package info
    """

    version_path = fake_keats.pkg().version_py()
    assert not isfile(version_path)
    fake_keats.version.up()
    assert isfile(version_path)

    pkg_info = fake_keats.info()

    with open(version_path, "r") as f:
        text = f.read()
        globals_ = {}
        exec(text, globals_)

        for k, v in pkg_info.items():
            key = "__{}__".format(k)
            assert key in globals_
            assert globals_[key] == v


class TestChangeLog:
    def test_bump_and_new(self, fake_keats):
        fake_keats.version.bump()
        fake_keats.changelog.new("new description", ["new changes"])

    def test_empty_changelog_up(self, fake_keats):
        fake_keats.changelog.up()

    def test_mark_as_released(self, fake_keats):
        fake_keats.version.bump()
        fake_keats.changelog.new("new description", ["new changes"])
        fake_keats.changelog.mark_as_released()


def test_bump(fake_keats):
    """We expect the version to be bump by one increment."""
    assert fake_keats.v() == "9.9.9"
    fake_keats.version.bump()
    assert fake_keats.v() == "9.9.10"


def test_bump_specific(fake_keats):
    """We expect the version to be bumped by user specified version."""
    assert fake_keats.v() == "9.9.9"
    fake_keats.version.bump("1.0.0")
    assert fake_keats.v() == "1.0.0"


def test_no_pyproject_toml(tmpdir):
    tmpdir.mkdir("testpackage")
    with pytest.raises(FileNotFoundError):
        Keats()
