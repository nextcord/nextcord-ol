from __future__ import annotations

from os import listdir
from os.path import isdir
from pathlib import Path

target = "nextcord_submodule/nextcord"
write = "nextcord_test"


tpath = Path(target)


def recursive_modules(module: Path) -> list[str]:
    modules = []

    for item in listdir(module):
        item = module / item
        if item.parts[-1] == "__pycache__":
            continue

        if isdir(item):
            for i, _ in enumerate(item.parts[2:]):
                modules.append(".".join(item.parts[2 + i :]))

            modules.extend(recursive_modules(item))

    return modules


modules = recursive_modules(tpath)
print(modules)
