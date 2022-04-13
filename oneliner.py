from os import makedirs
from pathlib import Path
from libcst import parse_module

from transformers import StatementTransformer


target = "nextcord_submodule/nextcord"
write = "nextcord_test"


def parse_file(path: Path) -> None:
    print(path)
    cst = parse_module(path.read_text())
    cst = cst.visit(StatementTransformer())

    path = Path(str(path).replace(target, write))
    makedirs(Path(*path.parts[:-1]), exist_ok=True)
    with open(path, "w") as f:
        f.write(cst.code)


def parse_directory(directory: Path) -> None:
    for file in directory.glob("**/*.py"):
        parse_file(file)


def main() -> None:
    parse_directory(Path(target))


if __name__ == "__main__":
    main()
