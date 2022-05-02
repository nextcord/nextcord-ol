# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING
from xml.dom.minidom import Attr

from libcst import Attribute, Call, CSTTransformer, Name, RemoveFromParent

if TYPE_CHECKING:
    from typing import TypeVar, Union

    from libcst import AnnAssign, Assign, FunctionDef, If, RemovalSentinel

    AS = TypeVar("AS", bound=Union[Assign, AnnAssign])


class TypingTransformer(CSTTransformer):
    """Removes unnecessary typing-specific nodes"""

    def __init__(self) -> None:
        self.type_checking_ifs: set[If] = set()
        """set of if statements to remove"""
        self.overload_funcs: set[FunctionDef] = set()
        """set of overload funcs to remove"""
        self.typevar_assigns: set[Assign | AnnAssign] = set()
        """set of typevar assignments to remove"""

    def visit_If(self, node: If) -> bool:
        test = node.test

        if (isinstance(test, Name) and test.value == "TYPE_CHECKING") or (
            isinstance(test, Attribute) and test.attr.value == "TYPE_CHECKING"
        ):
            self.type_checking_ifs.add(node)

        return False  # we dont need the body

    def leave_If(self, original: If, updated: If) -> If | RemovalSentinel:
        if original in self.type_checking_ifs:
            self.type_checking_ifs.discard(original)
            return RemoveFromParent()

        return updated

    def visit_FunctionDef(self, node: FunctionDef) -> bool:
        if not node.decorators:
            return False

        deco = node.decorators[0].decorator

        if (isinstance(deco, Name) and deco.value == "overload") or (
            isinstance(deco, Attribute) and deco.attr.value == "overload"
        ):
            self.overload_funcs.add(node)

        return False

    def leave_FunctionDef(
        self, original: FunctionDef, updated: FunctionDef
    ) -> FunctionDef | RemovalSentinel:
        if original in self.overload_funcs:
            self.overload_funcs.discard(original)
            return RemoveFromParent()

        return updated

    def visit_Assign(self, node: Assign) -> bool:
        return self.visit_assignment(node)

    def visit_AnnAssign(self, node: AnnAssign) -> bool:
        return self.visit_assignment(node)

    def visit_assignment(self, node: Assign | AnnAssign) -> bool:
        value = node.value

        if isinstance(value, Call) and (
            (isinstance(value.func, Name) and value.func.value == "TypeVar")
            or (
                isinstance(value.func, Attribute) and value.func.attr.value == "TypeVar"
            )
        ):
            self.typevar_assigns.add(node)

        return False

    def leave_Assign(
        self, original: Assign, updated: Assign
    ) -> Assign | RemovalSentinel:
        return self.leave_assignment(original, updated)

    def leave_AnnAssign(
        self, original: AnnAssign, updated: AnnAssign
    ) -> AnnAssign | RemovalSentinel:
        return self.leave_assignment(original, updated)

    def leave_assignment(self, original: AS, updated: AS) -> AS | RemovalSentinel:
        if original in self.typevar_assigns:
            self.typevar_assigns.discard(original)
            return RemoveFromParent()

        return updated
