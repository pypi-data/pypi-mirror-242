from __future__ import annotations

from pathlib import Path
from re import IGNORECASE, search
from subprocess import PIPE, CalledProcessError, check_output

from utilities.pathlib import PathLike

_GET_BRANCH_NAME = ["git", "rev-parse", "--abbrev-ref", "HEAD"]


def get_branch_name(*, cwd: PathLike = Path.cwd()) -> str:
    """Get the current branch name."""
    root = get_repo_root(cwd=cwd)
    output = check_output(
        _GET_BRANCH_NAME,  # noqa: S603
        stderr=PIPE,
        cwd=root,
        text=True,
    )
    return output.strip("\n")


def get_repo_name(*, cwd: PathLike = Path.cwd()) -> str:
    """Get the repo name."""
    root = get_repo_root(cwd=cwd)
    output = check_output(
        ["git", "remote", "get-url", "origin"],  # noqa: S603, S607
        stderr=PIPE,
        cwd=root,
        text=True,
    )
    return Path(output.strip("\n")).stem


def get_repo_root(*, cwd: PathLike = Path.cwd()) -> Path:
    """Get the repo root."""
    try:
        output = check_output(
            ["git", "rev-parse", "--show-toplevel"],  # noqa: S603, S607
            stderr=PIPE,
            cwd=cwd,
            text=True,
        )
    except CalledProcessError as error:
        # newer versions of git report "Not a git repository", whilst older
        # versions report "not a git repository"
        if search("fatal: not a git repository", error.stderr, flags=IGNORECASE):
            raise InvalidRepoError(cwd) from None
        raise  # pragma: no cover
    else:
        return Path(output.strip("\n"))


class InvalidRepoError(TypeError):
    """Raised when an invalid repo is encountered."""


__all__ = ["get_branch_name", "get_repo_name", "get_repo_root", "InvalidRepoError"]
