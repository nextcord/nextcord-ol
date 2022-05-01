from __future__ import annotations

from enum import Enum, auto
from typing import Literal, overload

from libcst import Attribute, BaseExpression, Name


class Type(Enum):
    NAME = auto()
    ATTRIBUTE = auto()


@overload
def highest(node: BaseExpression, type: Literal[Type.NAME]) -> Name:
    ...


@overload
def highest(node: BaseExpression, type: Literal[Type.ATTRIBUTE]) -> Attribute:
    ...


@overload
def highest(node: BaseExpression, type: Type) -> Name | Attribute:
    ...


def highest(node: BaseExpression, type: Type) -> Name | Attribute:
    """return the deepest name in the expression

    Parameters
    ----------
    node: :class:`libcst.BaseExpression`
        the expression to search
    type: :class:`Type`
        the type of node to return

    Example
    -------
    ::

        >>> highest_name(
                Attribute(
                    value=Attribute(
                        value=Name("x")
                        attr=Name("y")
                    ),
                    attr=Name("z"),
                )
            )

        Name("x")
    """

    if isinstance(node, Name):
        return node

    assert isinstance(node, Attribute)

    if isinstance(node.value, Name):
        return node if type is Type.NAME else node.value

    assert isinstance(node.value, Attribute)

    return highest(node.value, type=type)
