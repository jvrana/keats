from os.path import dirname, join, abspath, isfile

here = join(abspath(dirname(__file__)))
data = join(here, "data")


def test_version(fake_keats):
    """We expect the version to be correctly returned"""
    assert fake_keats.version() == "9.9.9"


def test_package(fake_keats):
    """We expect the package name to be correctly returned"""
    assert fake_keats.package() == "testpackage"


def test_format(fake_keats):
    """We expect a successfully implemented format"""
    fake_keats.format()


def test_version_json(fake_keats):
    """We expect the package info to be written to a version.py file.
    We then check the contents of that file with 'exec' and verify its
    contents with the package info"""

    version_path = fake_keats._version_py()
    assert not isfile(version_path)
    fake_keats.up()
    assert isfile(version_path)

    pkg_info = fake_keats.info()

    with open(version_path, "r") as f:
        text = f.read()
        globals = {}
        exec(text, globals)

        for k, v in pkg_info.items():
            key = "__{}__".format(k)
            assert key in globals
            assert globals[key] == v


def test_bump(fake_keats):
    """We expect the version to be bump by one increment"""
    assert fake_keats.version() == "9.9.9"
    fake_keats.bump()
    assert fake_keats.version() == "9.9.10"


def test_bump_specific(fake_keats):
    """We expect the version to be bumped by user specified version"""
    assert fake_keats.version() == "9.9.9"
    fake_keats.bump("1.0.0")
    assert fake_keats.version() == "1.0.0"
