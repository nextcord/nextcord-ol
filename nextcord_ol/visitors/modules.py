# SPX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING

from libcst import CSTVisitor

if TYPE_CHECKING:
    from typing import Optional

    from libcst import ImportFrom

__all__ = ("ModuleVisitor",)


class ModuleVisitor(CSTVisitor):
    """Visitor to collect all modules used in the target parent module."""                     

    def __init__(self) -> None:
        self.found_modules: set[str] = set()
        """Set of modules found in the target parent module."""

        self.just_directories: set[str] = set()
        """Directories found that are not separate modules."""

    def visit_ImportFrom(self, node: ImportFrom) -> Optional[bool]:
        if not node.relative:
            # Only care about relative imports
            return False

        return False
