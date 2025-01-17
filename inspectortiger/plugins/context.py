"""
## Context
Context management for AST

- `db['context']['context']` => Current context
- `db['context']['previous_contexts']` => Previous contexts
- `db['context']['next_contexts']` => Next contexts
- `db['context']['global_context']` => Global context
- `get_context(node, db)` => Infer context of given `node`
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
from enum import Enum, auto

from inspectortiger.inspector import Inspector
from inspectortiger.utils import Events

__author__ = "Batuhan Taskaya"


class Contexts(Enum):
    ANON = auto()  # comps + lambda
    CLASS = auto()
    GLOBAL = auto()
    FUNCTION = auto()


CTX_TYPES = {ast.ClassDef: Contexts.CLASS, ast.FunctionDef: Contexts.FUNCTION}


@dataclass
class Context:
    name: str
    context: Contexts
    kpair: KPair


@dataclass(unsafe_hash=True)
class KPair:
    start: int
    end: int

    @classmethod
    def from_node(cls, node):
        return cls(start=node.lineno, end=node.end_lineno)

    def distance(self, other):
        return (
            (self.start - other.start) ** 2 + (self.end - other.end) ** 2
        ) ** 0.5


def get_context(node, db):
    possible_contexts = []
    node_kpair = KPair.from_node(node)
    for kpair, context in db["context"]["next_contexts"].items():
        if node_kpair.start >= kpair.start and node_kpair.end <= kpair.end:
            possible_contexts.append((kpair.distance(node_kpair), context))

    possible_contexts.sort(key=lambda ctx: ctx[0])
    try:
        return possible_contexts[0][1]
    except IndexError:
        return db["context"]["global_context"]


@Inspector.register(ast.Module)
def prepare_contexts(node, db):
    db["context"]["global_context"] = global_ctx = Context(
        "__main__", Contexts.GLOBAL, KPair(0, 0)
    )
    db["context"]["previous_contexts"] = []
    db["context"]["context"] = global_ctx
    for possible_context in ast.walk(node):
        if isinstance(possible_context, tuple(CTX_TYPES)):
            kpair = KPair.from_node(possible_context)
            ctx = CTX_TYPES[type(possible_context)]
            ctx = Context(possible_context.name, ctx, kpair)
            db["context"]["next_contexts"][ctx.kpair] = ctx


@Inspector.register(ast.ClassDef, ast.FunctionDef)
def change_context(node, db):
    context = get_context(node, db)
    db["context"]["previous_contexts"].append(db["context"]["context"])
    db["context"]["context"] = context


@Inspector.on_event(Events.NODE_FINALIZE)
@Inspector.register(ast.ClassDef, ast.FunctionDef)
def finalize_context(node, db):
    context = db["context"]["previous_contexts"].pop()
    db["context"]["context"] = context
