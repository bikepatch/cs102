import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    header = f"{fmt} {len(data)}\0"
    stored_data = header.encode() + data
    hash_obj = hashlib.sha1(stored_data).hexdigest()
    if write:
        gitdir = repo_find()
        path = gitdir / "objects" / hash_obj[:2]
        (path).mkdir(exist_ok=True)
        with (path / hash_obj[2:]).open("wb") as f:
            f.write(zlib.compress(stored_data))
    return hash_obj


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    # PUT YOUR CODE HERE
    ...


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    # PUT YOUR CODE HERE
    ...


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    ...


def cat_file(obj_name: str, pretty: bool = True) -> None:
    # PUT YOUR CODE HERE
    ...


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
