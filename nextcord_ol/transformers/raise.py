from __future__ import annotations

from libcst import (
    Arg,
    Call,
    CSTTransformer,
    Expr,
    Raise,
    SimpleStatementLine,
    parse_expression,
)


class RaiseTransformer(CSTTransformer):
    """Edits raise statements to expressions (lambda-friendly)"""

    def __init__(self) -> None:
        self.edited_raises: dict[Raise, Expr] = {}
        """dict of raises to edited expression"""

    THROW = parse_expression("(_ for _ in ()).throw")
    EMPTY = parse_expression("sys.exc_info()[1]")

    def visit_Raise(self, node: Raise) -> bool:
        exc = self.THROW if node.exc else self.EMPTY
        self.edited_raises[node] = Expr(value=Call(func=self.THROW, args=[Arg(exc)]))

        return False  # no children for raising

    def leave_SimpleStatementLine(
        self, original: SimpleStatementLine, updated: SimpleStatementLine
    ) -> SimpleStatementLine:
        stmt = original.body[0]

        if isinstance(stmt, Raise):
            if stmt in self.edited_raises:
                u = updated.with_changes(body=[self.edited_raises[stmt]])
                del self.edited_raises[stmt]
                return u
            # unsure what to do about blank `raise` just yet

        return updated
