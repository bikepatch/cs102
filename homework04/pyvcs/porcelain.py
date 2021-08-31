import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import (
    commit_parse,
    find_object,
    find_tree_files,
    read_object,
    read_tree,
)
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths, True)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    tree = write_tree(gitdir, read_index(gitdir))
    return commit_tree(gitdir, tree=tree, message=message, author=author)


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    for entry in read_index(gitdir):
        if pathlib.Path(entry.name).exists():
            os.remove(entry.name)
    info = commit_parse(read_object(obj_name, gitdir)[1])
    running = True
    while running:
        trees = [(gitdir.parent, read_tree(read_object(info["tree"], gitdir)[1]))]
        while trees:
            tree_path, tree_info = trees.pop()
            for tree_data in tree_info:
                header, data = read_object(tree_data[1], gitdir)
                path = tree_path / tree_data[2]
                if header == "tree":
                    trees.append((path, read_tree(data)))
                    if not (path).exists():
                        (path).mkdir()
                else:
                    if not (path).exists():
                        with open(path, "wb") as f:
                            f.write(data)
                        (path).chmod(int(str(tree_data[0]), 8))
        if "parent" in info:
            info = commit_parse((read_object(info["parent"], gitdir)[1]))
        else:
            running = False
    for dirictory in gitdir.parent.glob("*"):
        if dirictory != gitdir and dirictory.is_dir():
            try:
                os.removedirs(dirictory)
            except OSError:
                continue
