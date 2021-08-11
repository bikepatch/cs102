import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    history = b""
    for entry in index:
        if "/" in entry.name:
            history += b"40000 "
            subdir = b""
            dirictory = entry.name[: entry.name.find("/")]
            history += dirictory.encode() + b"\0"
            subdir += oct(entry.mode)[2:].encode() + b" " + entry.name[entry.name.find("/") + 1 :].encode() + b"\0" + entry.sha1
            hash_obj = hash_object(subdir, fmt="tree", write=True)
            history += bytes.fromhex(hash_obj)
        else:
            history += oct(entry.mode)[2:].encode() + b" " + entry.name.encode() + b"\0" + entry.sha1
    tree = hash_object(history, fmt="tree", write=True)
    return tree


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    # PUT YOUR CODE HERE
    ...
