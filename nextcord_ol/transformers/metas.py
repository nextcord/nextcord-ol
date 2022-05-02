# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING

from libcst import CSTTransformer, Expr, RemoveFromParent, SimpleString

if TYPE_CHECKING:
    from libcst import Comment, RemovalSentinel, SimpleStatementLine


class MetaTransformer(CSTTransformer):
    """Remove code meta things such as module docstrings and comments"""

    def __init__(self) -> None:
        self.docstrings: set[SimpleStatementLine] = set()
        """set of docstrings to remove"""

    def visit_SimpleStatementLine(self, node: SimpleStatementLine) -> bool:
        if (
            node.body
            and isinstance(node.body[0], Expr)
            and isinstance(node.body[0].value, SimpleString)
            and node.body[0].value.value.startswith(('"""', "'''", "r'''", 'r"""'))
        ):
            self.docstrings.add(node)

        return False

    def leave_SimpleStatementLine(
        self, original: SimpleStatementLine, updated: SimpleStatementLine
    ) -> SimpleStatementLine | RemovalSentinel:
        if original in self.docstrings:
            return RemoveFromParent()

        return updated

    def leave_Comment(self, _: Comment, __: Comment) -> Comment | RemovalSentinel:
        return RemoveFromParent()
