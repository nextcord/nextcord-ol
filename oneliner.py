from os import makedirs
from pathlib import Path
from libcst import parse_module

# from transformers import StatementTransformer
# from transformers import ImportTransformer


target = "nextcord_submodule/nextcord"
write = "nextcord_test"


def parse_file(path: Path) -> None:
    cst = parse_module(path.read_text())
    # cst = cst.visit(StatementTransformer())

    path.write_text(cst.code)


def parse_directory(directory: Path) -> None:
    output = ""

    for file in directory.glob("**/*.py"):
        output += file.read_text() + "\n"

    path = Path("nextcord_test/onelined.py")

    path.write_text(output)

    parse_file(path)


def main() -> None:
    makedirs(write, exist_ok=True)

    parse_directory(Path(target))


if __name__ == "__main__":
    main()
