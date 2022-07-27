# SPDX-License-Identifier: MIT

from __future__ import annotations

from pathlib import Path

from libcst import parse_module

from nextcord_ol.config import target
from nextcord_ol.visitors import ModuleVisitor

target_path = Path(target)


with open(target_path / "__init__.py", mode="r") as f:
    init = parse_module(f.read())

module_visitor = ModuleVisitor()

init.visit(module_visitor)

found_modules = module_visitor.found_modules
just_directories = module_visitor.just_directories
