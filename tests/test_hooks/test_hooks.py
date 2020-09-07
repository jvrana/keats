from os.path import isfile
from os.path import join

import pytest

from keats import Keats
from keats.hooks.keats_version_up import logger
from keats.hooks.keats_version_up import main
from keats.hooks.keats_version_up import parse_args
from keats.hooks.utils import cmd_output


@pytest.fixture(autouse=True)
def reset_logger():
    level = logger.level
    yield
    logger.setLevel(level)


def pytest_addoption(parser):
    parser.addoption(
        "--log", action="store", default="WARNING", help="set logging level"
    )


class TestParseArgs:
    def test_parse_args_default(self):
        args = parse_args(argv=["f1", "f2"])
        assert args.filenames == ["f1", "f2"]
        assert args.verbose == 0

    def test_parse_args_none(self):
        args = parse_args(argv=None)
        assert args.filenames == []
        assert args.verbose == 0

    def test_parse_args_v(self):
        args = parse_args(argv=["f1", "f2", "-v"])
        assert args.filenames == ["f1", "f2"]
        assert args.verbose == 1

    def test_parse_args_vv(self):
        args = parse_args(argv=["f1", "f2", "-vv"])
        assert args.filenames == ["f1", "f2"]
        assert args.verbose == 2

    def test_parse_args_vvv(self):
        args = parse_args(argv=["f1", "f2", "-vvv"])
        assert args.filenames == ["f1", "f2"]
        assert args.verbose == 3


def test_temp_dir(temp_dir):
    assert isfile(join(temp_dir, "pyproject.toml"))
    with temp_dir.as_cwd():
        assert isfile("pyproject.toml")

    assert isfile(join(temp_dir, ".fixture"))
    with temp_dir.as_cwd():
        assert isfile(".fixture")


def test_version_missing(temp_dir):
    with temp_dir.as_cwd():
        # Should not fail with default
        temp_dir.join("f.py").write("a" * 10000)
        cmd_output("git", "add", "f.py")
        assert main(argv=["f.py"]) == 1


def test_adding_pyproject(temp_dir):
    with temp_dir.as_cwd():
        # Should not fail with default
        cmd_output("git", "add", "pyproject.toml")
        assert main(argv=["pyproject.toml"]) == 1


def test_version_not_changed(temp_dir):
    with temp_dir.as_cwd():
        assert not isfile(temp_dir.join("fakekeats/__version__.py"))
        # Should not fail with default
        keats = Keats()
        keats.version.up()
        assert isfile(temp_dir.join("fakekeats/__version__.py"))

        cmd_output("git", "add", "pyproject.toml")
        assert main(argv=["pyproject.toml"]) == 0


def test_version_changed(temp_dir):
    with temp_dir.as_cwd():
        assert not isfile(temp_dir.join("fakekeats/__version__.py"))
        # Should not fail with default
        keats = Keats()
        keats.version.up()
        assert isfile(temp_dir.join("fakekeats/__version__.py"))

        with open(temp_dir.join("fakekeats/__version__.py"), "a") as f:
            f.writelines(["# this is an extra line"])

        cmd_output("git", "add", "pyproject.toml")
        assert main(argv=["pyproject.toml"]) == 1


def test_update_pyproject(temp_dir):
    with temp_dir.as_cwd():
        assert not isfile(temp_dir.join("fakekeats/__version__.py"))
        # Should not fail with default
        keats = Keats()
        keats.version.up()
        assert isfile(temp_dir.join("fakekeats/__version__.py"))

        import toml

        with open("pyproject.toml", "r") as f:
            config = toml.load(f)

        config["tool"]["poetry"]["version"] = "1.0.0"
        with open("pyproject.toml", "w") as f:
            toml.dump(config, f)

        cmd_output("git", "add", "pyproject.toml")
        assert main(argv=["pyproject.toml"]) == 1

        with open("fakekeats/__version__.py", "r") as f:
            txt = f.read()
            assert '__version__ = "1.0.0"' in txt or "__version__ = '1.0.0'" in txt


def test_pass_none(temp_dir):
    with temp_dir.as_cwd():
        main(argv=None)


def test_verbose_vvv(temp_dir):
    with temp_dir.as_cwd():
        logger.setLevel("CRITICAL")
        print(logger.level)
        assert not logger.isEnabledFor(10)
        main(argv=["-vvv"])
        print(logger.level)
        assert logger.isEnabledFor(10)


def test_verbose_vv(temp_dir):
    with temp_dir.as_cwd():
        logger.setLevel("CRITICAL")
        print(logger.level)
        assert not logger.isEnabledFor(20)
        main(argv=["-vv"])
        print(logger.level)
        assert logger.isEnabledFor(20)
        assert not logger.isEnabledFor(10)


def test_verbose_v(temp_dir):
    with temp_dir.as_cwd():
        logger.setLevel("CRITICAL")
        print(logger.level)
        assert not logger.isEnabledFor(30)
        main(argv=["-v"])
        print(logger.level)
        assert logger.isEnabledFor(30)
        assert not logger.isEnabledFor(20)
