# SPDX-License-Identifier: MIT

from os import makedirs
from pathlib import Path

from libcst import parse_module

from .config import modules, target, write
from .transformers import ImportTransformer, TypingTransformer


def parse_file(path: Path) -> None:
    cst = parse_module(path.read_text())
    cst = cst.visit(ImportTransformer(path=path, modules=modules))
    cst = cst.visit(TypingTransformer())

    path = Path("/".join(path.parts).replace(target, write))
    makedirs("/".join(path.parts[:-1]), exist_ok=True)
    path.write_text(cst.code)


def parse_directory(directory: Path) -> None:
    for file in sorted(directory.glob("**/*.py")):
        print(file)
        if "__init__.py" in file.parts:
            continue

        parse_file(file)


def main() -> None:
    makedirs(write, exist_ok=True)

    parse_directory(Path(target))
    # parse_file(Path(target) / "__main__.py")


if __name__ == "__main__":
    main()
