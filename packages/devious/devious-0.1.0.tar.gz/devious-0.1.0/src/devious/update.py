"""Update utilities."""

import logging
import os
import shutil
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

import click

from devious.wrappers import git

logger = logging.getLogger()


@click.command()
@click.option("--private-remote", type=str)
@click.option(
    "--strategy",
    type=click.Choice(["squash", "merge", "rebase"]),
    default="squash",
    help="Set merge strategy for upstream commits.",
)
def update(private_remote: str, strategy: str) -> None:
    """Update dev environment if in a detached private repository. Will pull the latest upstream commits on your branch and push it.
    strategy: The way the update is applied, defaults to having a single squash commit."""

    devcontainer_repo_remote = "https://github.com/flxtrtwn/devcontainer.git"
    current_remote = git.query_remote()
    if current_remote == devcontainer_repo_remote:
        if not click.confirm(
            "Updating your environment will detach it from the upstream remote (flxtrtwn/devcontainer) "
            "and should only be used for private repositories where forking is not possible. Continue?"
        ):
            sys.exit(0)
        else:
            if not private_remote:
                logger.error("You need to specify --private-remote for the initial update setup.")
                sys.exit(1)
            devcontainer_repo_folder = Path("/tmp/devcontainer")
            devcontainer_repo_folder.mkdir(parents=True)
            git.remote_rename("origin", "upstream")
            git.remote_add("origin", private_remote)
            with switch_dir(devcontainer_repo_folder):
                git.clone(devcontainer_repo_remote, bare=True)
                git.push(mirror=True, remote=private_remote)
            shutil.rmtree(devcontainer_repo_folder)
            git.set_default_remote_for_branch()
    git.pull(remote="upstream", strategy=strategy)
    git.push()


@contextmanager
def switch_dir(dir: Path) -> Generator[None, Any, None]:
    current_dir = os.getcwd()
    os.chdir(dir)
    try:
        yield
    finally:
        os.chdir(current_dir)
