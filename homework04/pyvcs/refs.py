import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    path = gitdir / ref
    with open(path, "w") as file:
        file.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    # PUT YOUR CODE HERE
    pass


def ref_resolve(gitdir: pathlib.Path, refname: str) -> tp.Optional[str]:
    path = gitdir / refname
    if refname == "HEAD":
        with open(path, "r") as f:
            info = f.read()
        refname = info[info.find(" ") + 1 :].strip()
    path = gitdir / refname
    if path.exists() is not False:
        with open(path, "r") as f:
            info = f.read()
        return info
    else:
        return None


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    resolve = ref_resolve(gitdir, "HEAD")
    if resolve is not None:
        return resolve
    else:
        return None


def is_detached(gitdir: pathlib.Path) -> bool:
    path = gitdir / "HEAD"
    with open(path, "r") as f:
        info = f.read()
    if not info.startswith("ref:"):
        return True
    else:
        return False


def get_ref(gitdir: pathlib.Path) -> str:
    path = gitdir / "HEAD"
    with open(path, "r") as f:
        info = f.read()
    if is_detached(gitdir):
        return info
    else:
        ref = info[info.find(" ") + 1 :].strip()
        return ref
