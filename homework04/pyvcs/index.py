import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        length = len(self.name)
        package = struct.pack(
            f"!10I20sH{length}s{8 - (62 + length) % 8}x",
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            self.ino & 0xFFFFFFFF,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
            self.name.encode(),
        )
        return package

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        data_unpacked = struct.unpack(f"!10I20sH{len(data) - 62}s", data)
        datas = list(data_unpacked)
        datas[-1] = datas[-1].strip(b"\00").decode()
        return GitIndexEntry(*datas)


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    path = gitdir / "index"
    info = []
    if (path).exists():
        with (path).open("rb") as f:
            data = f.read()
        count = struct.unpack("!L", data[8:12])[0]
        start_pos = 12
        for i in range(count):
            end_pos = start_pos + 62 + data[start_pos + 62 :].find(b"\x00")
            entry = data[start_pos:end_pos]
            info.append(GitIndexEntry.unpack(entry))
            start_pos = end_pos + (8 - ((62 + len(info[i].name)) % 8))
    return info


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    info = struct.pack("!4sLL", b"DIRC", 2, len(entries))
    for entry in entries:
        info += entry.pack()
    info += bytes.fromhex(hashlib.sha1(info).hexdigest())
    with open(gitdir / "index", "wb") as f:
        f.write(info)


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    entries = read_index(gitdir)
    if details:
        for entry in entries:
            print(f"{entry.mode:o} {entry.sha1.hex()} 0\t{entry.name}")
    else:
        for entry in entries:
            print(entry.name)


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    entries = []
    for path in paths:
        with open(path, "r") as f:
            info = f.read()
        sha1 = hash_object(info.encode(), "blob", write=True)
        file = os.stat(path)
        entries.append(
            GitIndexEntry(
                ctime_s=round(file.st_ctime),
                ctime_n=0,
                mtime_s=round(file.st_mtime),
                mtime_n=0,
                dev=file.st_dev,
                ino=file.st_ino,
                mode=file.st_mode,
                uid=file.st_uid,
                gid=file.st_gid,
                size=file.st_size,
                sha1=bytes.fromhex(sha1),
                flags=len(path.name),
                name=str(path),
            )
        )

    if (gitdir / "index").exists():
        entry = read_index(gitdir)
        entry += entries
        write_index(gitdir, sorted(entry, key=lambda x: x.name))
    else:
        write_index(gitdir, sorted(entries, key=lambda x: x.name))
