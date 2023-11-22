from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from shutil import move, rmtree

from atomicwrites import move_atomic, replace_atomic

from utilities.errors import DirectoryExistsError
from utilities.pathlib import PathLike
from utilities.tempfile import TemporaryDirectory


@contextmanager
def writer(path: PathLike, /, *, overwrite: bool = False) -> Iterator[Path]:
    """Yield a path for atomically writing files to disk."""
    path = Path(path)
    parent = path.parent
    parent.mkdir(parents=True, exist_ok=True)
    name = path.name
    with TemporaryDirectory(suffix=".tmp", prefix=name, dir=parent) as temp_dir:
        try:
            yield (temp_path := temp_dir.joinpath(name))
        except KeyboardInterrupt:
            rmtree(temp_dir)
        else:
            src, dest = str(temp_path), str(path)
            if temp_path.is_file():
                if overwrite:
                    return replace_atomic(src, dest)
                return move_atomic(src, dest)
            if path.exists() and not overwrite:
                raise DirectoryExistsError(path)
            return move(src, dest)


__all__ = ["writer"]
