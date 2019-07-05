# make a change log

import datetime
from os.path import dirname, abspath, join, isfile
import json

from collections import OrderedDict
import sys


ENTRY_TEMPLATE = """
## {version}

**{date}**
{description}

{changes}
"""


def new_entry(d, changes):
    now = datetime.datetime.now()
    return {"description": d, "date": now.isoformat(), "changes": changes}


def to_markdown(data):
    s = "# changelog"

    entries = []
    for k, d in data.items():
        changes = "\n".join([" - " + c for c in d["changes"]])
        entry = ENTRY_TEMPLATE.format(
            version=k, date=d["date"], description=d["description"], changes=changes
        )
        entries.append(entry)
    s += "\n".join(entries)
    return s


def load(changelogpath):
    if isfile(changelogpath):
        with open(changelogpath, "r") as f:
            text = f.read()
            if text.strip() == "":
                changelog = []
            else:
                changelog = json.loads(text)
    else:
        changelog = {}

    sorted_entries = sorted(
        [(k, v) for k, v in changelog.items()], key=lambda x: x[1]["date"], reverse=True
    )
    return OrderedDict(sorted_entries)


def update(version, description, changes, changelogpath):
    changelog = load(changelogpath)

    if version in changelog:
        entry = changelog[version]
        entry["description"] = description

        now = datetime.datetime.now()
        entry["date"] = now.isoformat()
        unique_changes = []
        for e in entry["changes"] + changes:
            if e not in unique_changes:
                unique_changes.append(e)
        entry["changes"] = unique_changes
    else:
        entry = new_entry(description, changes)
    changelog[version] = entry
    with open(changelogpath, "w") as f:
        json.dump(changelog, f)


def save_to_markdown(changelogpath, path):
    with open(path, "w") as f:
        f.write(to_markdown(load(changelogpath)))


def update_changelog_interactive(version, changelogpath, markdownpath):
    print("****** Updating change log ({}) ******".format(version))
    description = input("Add a description: ")
    change_input = None
    changes = []
    while change_input != "":
        if change_input is not None:
            changes.append(change_input)
        change_input = input("List a change (ENTER to finish): ").strip()
    print(changes)
    update(version, description, changes, changelogpath)
    save_to_markdown(changelogpath, markdownpath)
