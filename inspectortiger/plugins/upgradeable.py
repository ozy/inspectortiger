""" Finds syntaxs that can be improved """

__author__ = "Batuhan Taskaya"
__version__ = "1.0.0"

import ast

from inspectortiger.inspector import Inspector
from inspectortiger.utils import Level, is_single_node, target_check


@Inspector.register(ast.For)
@Level.AVG
def yield_from(node, db):
    return (
        is_single_node(node, ast.Expr)
        and isinstance(node.body[0].value, ast.Yield)
        and target_check(node.body[0].value.value, node.target)
    )
