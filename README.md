# Keats

![John Keats](assets/keats.jpg)

Keats is an Python build, installation, and workflow manager.

Features include forced change logs, release scripts, and package version control.

## Why

Every Python developer seems to have their own tricks and scripts for
maintaining changelogs, package versions, and managing releases. Rather
than reinventing the wheel everytime you develop a new pacakge, Keats
provides a standard workflow package release workflow using Poetry. All
of this is provided with a commandline interface.

## Usage

```
keats bump <VERSION>
```

```
# get the package version number
keats version
```

## Installation


```
# globally install keats
pip install keats
```

```
# locally install keats
poetry add --dev keats

# run keats
poetry run keats
```