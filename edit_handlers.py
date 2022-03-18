#!/usr/bin/env python3
# A program to revert default settings on mimetype handlers changed by Mozilla
# on Firefox 98 unilaterally and without consultation of the community
# (as it is too often the case).
#
# Copyright (C) 2022 Ysard - <ysard@users.noreply.github.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
from pathlib import Path
import shutil
import json
import argparse


DEFAULT_ACTION = 1
DEFAULT_ASK = True


def edit_handlers(input_file, output):
    """Open handlers.json and edit a new version with the default behavior
    for downloaded files changed
    """
    content = Path(input_file).read_text()
    json_data = json.loads(content)

    # We are interested only in mimetypes
    mimetypes = json_data["mimeTypes"]

    for mimetype, settings in mimetypes.items():
        if settings.get("action") == 0 and settings.get("ask") == False:
            settings["action"] = DEFAULT_ACTION
            settings["ask"] = DEFAULT_ASK

    # Overwrite our new rules
    json_data["mimeTypes"] = mimetypes

    # Export the new file content
    Path(output).write_text(json.dumps(json_data, sort_keys=True))


def args_to_params(args):
    """Return argparse namespace as a dict {variable name: value}"""
    return dict(vars(args).items())


def test_args(args):
    """Validate given arguments

    - Test input file
    - Try to backup the input file
    - If the backup file already exists, ask what to do
    """
    if not Path(args.input_file).exists():
        print("Given file doesn't exist:", args.input_file)
    elif Path(args.input_file + ".bak").exists():
        # Backup already exists => ask if we should continue
        print(
            "The backup file '{}.bak' will be overwritten by the current '{}' file.".format(
                args.input_file, args.input_file
            )
        )
        ret = None
        while ret not in ("Y", "y", "N", "n"):
            ret = input("Do you want to process ? Y/N ")

        if ret in ("N", "n"):
            exit()
    # Make backup
    shutil.copy(args.input_file, args.input_file + ".bak")


def main():
    """Entry point and argument parser"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "input_file",
        nargs="?",
        help="handlers.json file path in the Firefox profile "
        "(on GNU/Linux: ~/.mozilla/firefox/<my_profile/). "
        "By default it will be renamed by adding a .bak suffix.",
        default="./handlers.json",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output filepath for the new JSON file.",
        default="./handlers.json",
    )

    # Get program args and launch associated command
    args = parser.parse_args()
    test_args(args)
    edit_handlers(**args_to_params(args))


if __name__ == "__main__":
    main()
