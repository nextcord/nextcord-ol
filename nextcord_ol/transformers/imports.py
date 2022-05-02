# SPDX-License-Identifier: MIT

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING

from libcst import (
    Arg,
    Attribute,
    Call,
    CSTTransformer,
    Decorator,
    Import,
    ImportAlias,
    ImportFrom,
    ImportStar,
    Name,
    Param,
    RemovalSentinel,
    RemoveFromParent,
    Return,
    SimpleStatementLine,
    Subscript,
)
from libcst.helpers import get_full_name_for_node_or_raise as get_full_name
from nextcord_ol.utils import Type, highest

if TYPE_CHECKING:
    from typing import TypeVar

    from libcst import CSTNode

    NODE = TypeVar("NODE", bound=CSTNode)


class ImportTransformer(CSTTransformer):
    """Modifies imports to be all absolute, deletes relative imports"""

    def __init__(self, path: Path, modules: list[str]) -> None:
        self.path = path
        """path to current file"""
        self.modules = modules
        """list of modules to delete imports from"""

        self.edited_statements: dict[str, Attribute] = {}
        """name to the full attribute"""
        self.edited_imports: dict[ImportFrom, Import] = {}
        """module to edited"""
        self.deleted_imports: set[ImportFrom] = set()
        """relative imports to delete"""

    def visit_ImportFrom(self, node: ImportFrom) -> bool:
        if isinstance(node.names, ImportStar):
            name = node.module

            if name is None:
                raise RuntimeError("HELP")
            elif isinstance(name, Attribute):
                name = Name(get_full_name(name))

            package = ".".join(self.path.parts[:-1])
            addon = "." * len(node.relative)

            mod = import_module(name=addon + name.value, package=package)

            for item in mod.__all__:
                self.edited_statements[item] = Attribute(
                    value=Name(name.value), attr=Name(item)
                )

            if not node.relative:
                self.edited_imports[node] = Import(names=[ImportAlias(name=name)])
        elif (
            node.module is None
            or node.relative
            or get_full_name(node.module) in self.modules
            or (isinstance(node.module, Name) and node.module.value == "__future__")
        ):
            self.deleted_imports.add(node)
        else:
            self.edited_imports[node] = Import(names=[ImportAlias(name=node.module)])

            for item in node.names:
                if isinstance(item.name, Attribute):
                    name = Name(value=highest(item.name, type=Type.NAME).value)
                else:
                    name = item.name if not item.asname else item.asname.name

                assert isinstance(name, Name)

                self.edited_statements[name.value] = Attribute(
                    value=node.module, attr=name
                )

        return False  # no children for importing

    def leave_ImportFrom(
        self, original: ImportFrom, updated: ImportFrom
    ) -> ImportFrom | RemovalSentinel:
        if original in self.deleted_imports:
            return RemoveFromParent()

        return updated

    def leave_SimpleStatementLine(
        self, original: SimpleStatementLine, updated: SimpleStatementLine
    ) -> SimpleStatementLine:
        stmt = original.body[0]

        if isinstance(stmt, ImportFrom):
            if stmt in self.edited_imports:
                u = updated.with_changes(body=[self.edited_imports[stmt]])
                del self.edited_imports[stmt]
                return u

        return updated

    def leave_Attribute(self, original: Attribute, updated: Attribute) -> Attribute:
        return self.edit(original, updated, attr="value")

    def leave_Call(self, original: Call, updated: Call) -> Call:
        return self.edit(original, updated, attr="func")

    def leave_Arg(self, original: Arg, updated: Arg) -> Arg:
        return self.edit(original, updated, attr="value")

    def leave_Param(self, original: Param, updated: Param) -> Param:
        return self.edit(original, updated, attr="default")

    def leave_Return(self, original: Return, updated: Return) -> Return:
        return self.edit(original, updated, attr="value")

    def leave_Decorator(self, original: Decorator, updated: Decorator) -> Decorator:
        return self.edit(original, updated, attr="decorator")

    def leave_Subscript(self, original: Subscript, updated: Subscript) -> Subscript:
        return self.edit(original, updated, attr="value")

    def edit(self, original: NODE, updated: NODE, *, attr: str) -> NODE:
        if isinstance(getattr(original, attr), Name):
            if getattr(original, attr).value in self.edited_statements:
                return updated.with_changes(
                    **{attr: self.edited_statements[getattr(original, attr).value]}
                )

        return updated
