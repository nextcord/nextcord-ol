from __future__ import annotations

from libcst import (
    Attribute,
    Expr,
    Name,
    GeneratorExp,
    CompFor,
    Tuple,
    Call,
    Arg,
    CSTTransformer,
    Raise,
    SimpleStatementLine,
)


class StatementTransformer(CSTTransformer):
    def __init__(self) -> None:
        self.edited_raises: dict[Raise, Expr] = {}

    THROW = Attribute(
        value=GeneratorExp(
            elt=Name(value="_"),
            for_in=CompFor(target=Name(value="_"), iter=Tuple(elements=[])),
        ),
        attr=Name(value="throw"),
    )
    # (_ for _ in ()).throw

    def visit_Raise(self, node: Raise) -> bool:
        """Find any raises and store their edited versions"""

        if node.exc is not None:
            self.edited_raises[node] = Expr(
                value=Call(
                    func=self.THROW,
                    args=[
                        Arg(node.exc),
                    ],
                )
            )

        # unsure what to do with empty raises

        return False  # no children for raising

    def leave_SimpleStatementLine(
        self, original: SimpleStatementLine, updated: SimpleStatementLine
    ) -> SimpleStatementLine:
        """Edit any raises with their new versions"""

        stmt = original.body[0]

        if isinstance(stmt, Raise):
            if stmt in self.edited_raises:
                u = updated.with_changes(body=[self.edited_raises[stmt]])
                del self.edited_raises[stmt]
                return u
            # unsure what to do about blank `raise` just yet

        return original
