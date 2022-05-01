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


class StatementTransformer(CSTTransformer):
    def __init__(self) -> None:
        self.edited_raises: dict[Raise, Expr] = {}
        """dict of raises to edited expression"""

    THROW = parse_expression("(_ for _ in ()).throw")

    def visit_Raise(self, node: Raise) -> bool:
        if node.exc is not None:
            self.edited_raises[node] = Expr(
                value=Call(
                    func=self.THROW,
                    args=[
                        Arg(node.exc),
                    ],
                )
            )

        # TODO: empty raises, sys_exc_info helps with that

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
