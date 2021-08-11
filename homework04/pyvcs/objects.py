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
    if len(obj_name) < 4 or len(obj_name) > 40:
        raise Exception(f"Not a valid object name {obj_name}")
    obj = []
    path = repo_find(gitdir) / "objects" / obj_name[:2]
    for file in (path).glob(f"{obj_name[2:]}*"):
        obj.append(obj_name[:2] + file.name)
    if len(obj) == 0:
        raise Exception(f"Not a valid object name {obj_name}")
    return obj


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    path = repo_find(gitdir) / "objects" / sha[:2] 
    with open(path / sha[2:], "rb") as f:
        z_data = zlib.decompress(f.read())
    header = z_data.split(b" ")[0]
    obj = z_data[z_data.find(b"\x00") + 1 :]
    return header.decode(), obj


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    tree = []
    while len(data) != 0:
        data = data[data.find(b" ") + 1 :]
        data = data[data.find(b"\x00") + 1 :]
        sha = bytes.hex(data[:20])
        mode = int(data[: data.find(b" ")].decode())
        name = data[: data.find(b"\x00")].decode()
        data = data[20:]
        tree.append((mode, name, sha))
    return tree


def cat_file(obj_name: str, pretty: bool = True) -> None:
    repo = repo_find()
    header, data = read_object(obj_name, repo)
    if header in ["blob", "commit"]:
        print(data.decode())
    else:
        for leaf in read_tree(data):
            if i[0] == 40000:
                print(f"{leaf[0]:06}", "tree", leaf[1] + "\t" + leaf[2])
            else:
                print(f"{leaf[0]:06}", "blob", leaf[1] + "\t" + leaf[2])


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
