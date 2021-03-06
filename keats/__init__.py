import os
import shutil
from collections import OrderedDict
from functools import wraps
from os.path import abspath
from os.path import dirname
from os.path import isdir
from os.path import isfile
from os.path import join

import fire
import toml
from termcolor import cprint

from .__version__ import __name__
from .__version__ import __version__
from .changelog_utils import ChangeLogWriter
from .utils import write_safe_file
from .utils import writelines_safe_file


PYPROJECT = "pyproject.toml"
RED = "\u001b[31m"
RESET = "\u001b[0m"
VERSIONPY = "__version__.py"


def err(msg):
    return cprint(msg, "red")


def info(msg):
    return cprint(msg, "blue")


keats_version = __name__ + " " + __version__
generated_by_keats = "# autogenerated by {}".format(keats_version)


class Pkg:
    def __init__(self, directory, filename):
        self.path = join(str(directory), str(filename))
        self.directory = directory

    def valid(self):
        return isfile(self.path)

    def _get(self, key):
        return self.get_config()["tool"]["poetry"].get(key, None)

    def get_config(self):
        """Return the toml file information.

        :return:
        :rtype:
        """

        return toml.load(self.path)

    def config_info(self):
        toml_info = OrderedDict(self.get_config()["tool"]["poetry"])
        pkg_info = {
            "version": toml_info["version"],
            "name": toml_info["name"],
            "title": toml_info["name"],
            "authors": toml_info.get("authors", list()),
            "repository": toml_info.get("repository", None),
            "homepage": toml_info.get("homepage", None),
            "description": toml_info.get("description", None),
            "license": toml_info.get("license", None),
            "maintainers": toml_info.get("maintainers", None),
            "readme": toml_info.get("readme", None),
        }
        return pkg_info

    def version_py(self):
        return join(self.pkg_path(), VERSIONPY)

    def local_path(self, path):
        return abspath(join(self.directory, path))

    def pkg_path(self):
        return self.local_path(self.package())

    def test_path(self):
        return self.local_path("tests")

    def packages(self):
        """Return all listed packaged in the pyproject.toml file. Note that
        this.

        does not consider * files.

        :return: list of package names
        :rtype: list
        """
        if "packages" in self.get_config()["tool"]["poetry"]:
            pkgs = []
            for pkg in self.get_config()["tool"]["poetry"]["packages"]:
                if "from" in pkg:
                    pkgs.append(join(pkg["from"], pkg["include"]))
                else:
                    pkgs.append(pkg["include"])
        else:
            pkgs = [self._get("name")]
        return pkgs

    def dependencies(self):
        return self.get_config()["tool"]["poetry"]["dependencies"]

    def dev_dependencies(self):
        return self.get_config["tool"]["poetry"]["dev-dependencies"]

    def name(self):
        return self._get("name")

    def package(self):
        """Return the estimated main package from the pyproject.toml file.

        :return: version
        :rtype: basestring
        """
        return self.packages()[0]

    def run_cmd(self, *cmd):
        cline = "(cd {}; {})".format(self.directory, " ".join(cmd))
        cprint("spawning shell ({})".format(self.directory), "blue")
        cprint(" ".join(cmd), "yellow")
        cprint("exiting shell", "blue")
        return os.system(cline)

    def run_poetry_cmd(self, *cmd):
        return self.run_cmd("poetry run", *cmd)


def requires_config(f):
    """If config is unavailable, prints a warning and does an early exit."""

    @wraps(f)
    def wrapped(self, *args, **kwargs):
        if not self._pkg.valid():
            print(err("No pyproject.toml file found"))
            exit(0)
        else:
            return f(self, *args, **kwargs)

    return wrapped


class Base:
    def __init__(self, path):
        self._pkg = path

    def _cmd(self, *cmd):
        return self._pkg.run_cmd(*cmd)

    @requires_config
    def _get(self, key):
        return self._pkg.get_config()["tool"]["poetry"].get(key, None)


class Run(Base):
    @requires_config
    def format(self):
        """Run the format script.

        :return:
        :rtype:
        """
        paths = [self._pkg.local_path(p) for p in self._pkg.packages() + ["tests"]]
        self._cmd(" ".join(["black"] + paths))

    @requires_config
    def _script(self, name):
        here = abspath(dirname(__file__))
        return join(here, "..", "keat_scripts", name)

    @requires_config
    def release(self):
        self._cmd("sh {}".format(self._script("release.sh")))

    @requires_config
    def document(self):
        pass

    def clear_cache(self, cachename="pypi"):
        info("clearing poetry cache")
        self._cmd("poetry cache:clear --all {}".format(cachename))

    def update(self, cache="pypi"):
        """Update keats in this project.

        :param clear: if provided, will clear the poetry cache (default: pypi)

        :return:
        """
        self._cmd("poetry remove --dev keats")
        if cache:
            self.clear_cache(cache)
        self.install()


class Version(Base):
    @requires_config
    def print(self):
        """Return package version."""
        return self._get("version")

    @requires_config
    def bump(self, version=None):
        if version is None:
            self._cmd("poetry version")
        else:
            self._cmd("poetry version {}".format(version))
        self._write()

    @requires_config
    def up(self, version=None):
        """Update the package version from the pyproject.toml file.

        :param version: if provided, bump the version number (optional)
        :type version: basestring
        :return: the version
        :rtype: basestring
        """
        if version is None:
            self._write()
        else:
            self.bump(version)
        return self._get("version")

    def _get_version_path(self):
        return self._pkg.version_py()

    def _exists(self):
        return isfile(self._get_version_path())

    def _version_str(self):
        pkg_info = self._pkg.config_info()
        lines = ["# {}\n".format(VERSIONPY), generated_by_keats + "\n"]
        for k, v in pkg_info.items():
            if isinstance(v, str):
                v = '"{}"'.format(v)
            lines.append("__{}__ = {}".format(k, v))
        return "\n".join(lines)

    def _version_changed(self) -> bool:
        if not isfile(self._get_version_path()):
            return True
        with open(self._get_version_path(), "r") as f:
            existing = f.read()

        lines1 = existing.splitlines()
        lines2 = self._version_str().splitlines()

        def clean(lines):
            lines = [l.strip() for l in lines]
            lines = [l for l in lines if len(l) > 1]
            lines = [l for l in lines if not l.startswith("#")]
            lines = [l for l in lines if not l.startswith("'''")]
            lines = [l for l in lines if not l.startswith('"""')]
            return lines

        lines1 = clean(lines1)
        lines2 = clean(lines2)

        return sorted(set(lines1)) != sorted(set(lines2))

    @requires_config
    def _write(self, with_confirm=False):
        path = self._get_version_path()
        if with_confirm:
            ans = input("Write to '{}'?".format(path))
        else:
            ans = ""
        if ans.strip() == "" or ans.strip().lower() == "y":
            if self._version_changed():
                write_safe_file(path, self._version_str())
        else:
            info("no files written")


class ChangeLog(Base):
    def __init__(self, path):
        super().__init__(path)
        path = join(self._dir(), "changelog.json")
        mdpath = join(self._dir(), "changelog.md")
        title = self._pkg.name()
        self.writer = ChangeLogWriter(path=path, title=title, mdpath=mdpath)

    @requires_config
    def _dir(self):
        d = join(self._pkg.directory, ".keats")
        if not isdir(d):
            os.mkdir(d)
        return d

    @requires_config
    def up(self):
        """Save changelog to a markdown file."""
        self.writer.save_to_markdown()

    @requires_config
    def clear(self):
        """Clear the changelog files."""
        if isfile(self.writer.path):
            os.remove(self.writer.path)
        if isfile(self.writer.mdpath):
            os.remove(self.writer.mdpath)

    @requires_config
    def mark_as_released(self):
        self.writer.mark_as_released(self._get("version"))

    @requires_config
    def new(self, description=None, changes=None):
        """Interactively add a changelog entry.

        Entries are located in the '.keats' folder.
        """
        self.writer.update_interactive(
            self._get("version"), description=description, changes=changes
        )


class TemporaryPath:
    def __init__(self, path):
        self.path = path
        self.existed = isfile(path)

    def __enter__(self):
        pass

    def __exit__(self, exception_type, exception_value, traceback):
        if not self.existed and isfile(self.path):
            os.remove(self.path)


class TemporaryFileWriter(TemporaryPath):
    def __enter__(self):
        self.file = open(self.path, "w")
        return self.file

    def __exit__(self, exception_type, exception_value, traceback):
        self.file.close()
        super().__exit__(exception_type, exception_value, traceback)


class Keats:
    """Python version and worfklow release manager.

    Usage `keats [command] [arguments]`
    """

    def __init__(self, directory=None, filename=PYPROJECT):
        if directory is None:
            directory = os.getcwd()
        self._pkg = Pkg(str(directory), str(filename))
        self._validate()

    def _validate(self):
        self._validate_config()
        self._validate_pkg_path()

    def _validate_config(self):
        pkg = self._pkg
        if not isfile(pkg.path):
            raise FileNotFoundError(
                "pyproject.toml was expected at {}".format(pkg.local_path(pkg.path))
            )

    def _validate_pkg_path(self):
        pkg = self._pkg
        pkg_path = pkg.local_path(pkg.package())
        if not isdir(pkg_path):
            raise NotADirectoryError(
                "Expecting package directory '{}'. Make sure this directory is defined "
                "correctly in `pyproject.toml`. If the package directory is included "
                "in [tool.poetry.packages], make sure it is the first entry as this "
                "is where keats expects to find the directory.".format(pkg_path)
            )

    def pkg(self):
        return self._pkg

    @requires_config
    def info(self):
        """Return package information from the toml file.

        :return:
        :rtype:
        """
        return self._pkg.config_info()

    @staticmethod
    def keats():
        """Return the keats version number.

        :return:
        :rtype:
        """
        return __name__ + " " + __version__

    @requires_config
    def v(self):
        """Return package version."""
        return self.version.print()

    @requires_config
    def name(self):
        return self._pkg.name()

    @requires_config
    def package(self):
        return self._pkg.package()

    @requires_config
    def packages(self):
        return self._pkg.packages()

    @property
    def version(self):
        return Version(self._pkg)

    @property
    def changelog(self):
        return ChangeLog(self._pkg)

    @property
    def run(self):
        return Run(self._pkg)

    def bump(self, version=None, description=None, changes=None):
        self.version.bump(version)
        self.changelog.new(description=description, changes=changes)

    def release(self):
        return self.run.release()

    def install(self):
        """Install keats to this project.

        :return:
        """
        self.run._cmd("poetry add --dev keats")
        self.up()

    def up(self):
        """Update .keats/changelog.json and __version__.py.

        :return:
        :rtype:
        """
        self.version.up()
        self.changelog.up()

    @requires_config
    def global_install(self, *args, cmd="pip install ."):
        """Pip install in editable mode. If not setup.py exists, creates a
        minimal setup.py.

        :param args:
        :type args:
        :return:
        :rtype:
        """
        path = self._pkg.local_path("setup.py")
        if not isfile(path):
            with TemporaryFileWriter(path) as f:
                lines = [
                    generated_by_keats + "\n",
                    "from distutils.core import setup\n",
                    "\n",
                    'setup(title="{title}", name="{name}", '
                    'version="{version}", packages={packages})\n'.format(
                        title=self.name(),
                        name=self.name(),
                        version=self.v(),
                        packages=self.packages(),
                    ),
                ]
                f.writelines(lines)
                self._pkg.run_cmd(cmd, *args)
        else:
            self._pkg.run_cmd(cmd, *args)

    @staticmethod
    def clean_dist():
        """Removes 'dist' and 'pip-wheel-metadata' if they exist.

        :return:
        :rtype:
        """
        folders = ["dist", "pip-wheel-metadata"]

        for folder in folders:
            if isdir(folder):
                shutil.rmtree(folder)

    # TODO: flesh this out with Jinja? When do we need a full setup.py file?
    @requires_config
    def develop(self, *args):
        """Pip install in editable mode. If not setup.py exists, creates a
        minimal setup.py.

        :param args:
        :type args:
        :return:
        :rtype:
        """
        self.clean_dist()
        setup = join(self._pkg.directory, "setup.py")
        requirements = join(self._pkg.directory, "requirements.txt")
        if isfile(setup):
            print("Creating temporary setup.py files")
            do_remove = True
            self.run._cmd("poetry-setup")
        else:
            do_remove = False
        self.global_install(*args, cmd="pip install -e .")
        if do_remove:
            print("Removing setup files")
            os.remove(setup)
            os.remove(requirements)


def main():
    fire.Fire(Keats)
