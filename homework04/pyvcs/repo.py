import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    gitdir = os.getenv("GIT_DIR", ".pyvcs")
    workdir = pathlib.Path(workdir)
    path = workdir / gitdir
    while pathlib.Path("/") != workdir.absolute():
        if (path).is_dir():
            return path
        workdir = workdir.parent
        path = workdir / gitdir
    if (path).is_dir():
        return path
    else:
        raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    gitdir = os.getenv("GIT_DIR", ".pyvcs")
    workdir = pathlib.Path(workdir)
    if workdir.is_file():
        raise Exception(f"{workdir} is not a directory")
    path = workdir / gitdir
    os.makedirs(path / "refs" / "heads", exist_ok=True)
    os.makedirs(path / "refs" / "tags", exist_ok=True)
    (path / "objects").mkdir()
    with open(path / "config", "w") as f:
        f.write(
            "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n",
        )
    with open(path / "HEAD", "w") as f:
        f.write("ref: refs/heads/master\n")
    with open(path / "description", "w") as f:
        f.write("Unnamed pyvcs repository.\n")
    return path
