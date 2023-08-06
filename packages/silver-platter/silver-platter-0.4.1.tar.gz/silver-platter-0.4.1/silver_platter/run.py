#!/usr/bin/python3
# Copyright (C) 2018 Jelmer Vernooij <jelmer@jelmer.uk>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

"""Automatic proposal/push creation."""

import argparse
import logging
import os
import subprocess
import sys
from typing import Optional, List

import silver_platter  # noqa: F401

from breezy import osutils
from breezy import errors
from breezy.commit import PointlessCommit
from breezy.workingtree import WorkingTree
from breezy import propose as _mod_propose
from .proposal import (
    UnsupportedHoster,
    enable_tag_pushing,
    find_existing_proposed,
    get_hoster,
)
from .workspace import (
    Workspace,
)
from .publish import (
    SUPPORTED_MODES,
)
from .utils import (
    open_branch,
    BranchMissing,
    BranchUnsupported,
    BranchUnavailable,
    full_branch_url,
)


class ScriptMadeNoChanges(errors.BzrError):

    _fmt = "Script made no changes."


def script_runner(
    local_tree: WorkingTree, script: str, commit_pending: Optional[bool] = None
) -> str:
    """Run a script in a tree and commit the result.

    This ignores newly added files.

    :param local_tree: Local tree to run script in
    :param script: Script to run
    :param commit_pending: Whether to commit pending changes
        (True, False or None: only commit if there were no commits by the
         script)
    :return: Description as reported by script
    """
    last_revision = local_tree.last_revision()
    p = subprocess.Popen(
        script, cwd=local_tree.basedir, stdout=subprocess.PIPE, shell=True
    )
    (description_encoded, err) = p.communicate(b"")
    if p.returncode != 0:
        raise errors.BzrCommandError(
            "Script %s failed with error code %d" % (script, p.returncode)
        )
    new_revision = local_tree.last_revision()
    description = description_encoded.decode()
    if last_revision == new_revision and commit_pending is None:
        # Automatically commit pending changes if the script did not
        # touch the branch.
        commit_pending = True
    if commit_pending:
        try:
            new_revision = local_tree.commit(description, allow_pointless=False)
        except PointlessCommit:
            pass
    if new_revision == last_revision:
        raise ScriptMadeNoChanges()
    return description


def derived_branch_name(script: str) -> str:
    return os.path.splitext(osutils.basename(script.split(" ")[0]))[0]


def main(argv: List[str]) -> Optional[int]:  # noqa: C901
    parser = argparse.ArgumentParser()
    parser.add_argument("script", help="Path to script to run.", type=str)
    parser.add_argument("url", help="URL of branch to work on.", type=str)
    parser.add_argument(
        "--derived-owner", type=str, default=None, help="Owner for derived branches."
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Refresh changes if branch already exists",
    )
    parser.add_argument(
        "--label", type=str, help="Label to attach", action="append", default=[]
    )
    parser.add_argument("--name", type=str, help="Proposed branch name", default=None)
    parser.add_argument(
        "--diff", action="store_true", help="Show diff of generated changes."
    )
    parser.add_argument(
        "--mode",
        help="Mode for pushing",
        choices=SUPPORTED_MODES,
        default="propose",
        type=str,
    )
    parser.add_argument(
        "--commit-pending",
        help="Commit pending changes after script.",
        choices=["yes", "no", "auto"],
        default="auto",
        type=str,
    )
    parser.add_argument(
        "--dry-run",
        help="Create branches but don't push or propose anything.",
        action="store_true",
        default=False,
    )
    args = parser.parse_args(argv)

    try:
        main_branch = open_branch(args.url)
    except (BranchUnavailable, BranchMissing, BranchUnsupported) as e:
        logging.exception("%s: %s", args.url, e)
        return 1

    if args.name is None:
        name = derived_branch_name(args.script)
    else:
        name = args.name
    commit_pending = {"auto": None, "yes": True, "no": False}[args.commit_pending]

    overwrite = False

    try:
        hoster = get_hoster(main_branch)
    except UnsupportedHoster as e:
        if args.mode != "push":
            raise
        # We can't figure out what branch to resume from when there's no hoster
        # that can tell us.
        resume_branch = None
        existing_proposal = None
        logging.warn(
            "Unsupported hoster (%s), will attempt to push to %s",
            e,
            full_branch_url(main_branch),
        )
    else:
        (resume_branch, resume_overwrite, existing_proposal) = find_existing_proposed(
            main_branch, hoster, name, owner=args.derived_owner
        )
        if resume_overwrite is not None:
            overwrite = resume_overwrite
    if args.refresh:
        resume_branch = None
    with Workspace(main_branch, resume_branch=resume_branch) as ws:
        try:
            description = script_runner(ws.local_tree, args.script, commit_pending)
        except ScriptMadeNoChanges:
            logging.exception("Script did not make any changes.")
            return 1

        def get_description(description_format, existing_proposal):
            if description is not None:
                return description
            if existing_proposal is not None:
                return existing_proposal.get_description()
            raise ValueError("No description available")

        enable_tag_pushing(ws.local_tree.branch)

        try:
            publish_result = ws.publish_changes(
                args.mode,
                name,
                get_proposal_description=get_description,
                dry_run=args.dry_run,
                hoster=hoster,
                labels=args.label,
                overwrite_existing=overwrite,
                derived_owner=args.derived_owner,
                existing_proposal=existing_proposal,
            )
        except UnsupportedHoster as e:
            logging.exception(
                "No known supported hoster for %s. Run 'svp login'?",
                full_branch_url(e.branch),
            )
            return 1
        except _mod_propose.HosterLoginRequired as e:
            logging.exception(
                "Credentials for hosting site at %r missing. " "Run 'svp login'?",
                e.hoster.base_url,
            )
            return 1

        if publish_result.proposal:
            if publish_result.is_new:
                logging.info("Merge proposal created.")
            else:
                logging.info("Merge proposal updated.")
            if publish_result.proposal.url:
                logging.info("URL: %s", publish_result.proposal.url)
            logging.info("Description: %s", publish_result.proposal.get_description())

        if args.diff:
            ws.show_diff(sys.stdout.buffer)

    return None


if __name__ == "__main__":
    sys.exit(main(sys.argv))
