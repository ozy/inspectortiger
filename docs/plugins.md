# Plugins
InspectorTiger plugins


## Context
Context management for AST

- `db['context']['context']` => Current context
- `db['context']['previous_contexts']` => Previous contexts
- `db['context']['next_contexts']` => Next contexts
- `db['context']['global_context']` => Global context
- `get_context(node, db)` => Infer context of given `node`

## Misc
Common gotchas


## Parentize
`parent` field to each node

- `parent_to(child, node)` => yields all parents of child until it reaches `node`

## Unreachable Except
Unreacable excepts

- `db['unreachable_except']['user_exceptions']` => A mapping of user-defined exceptions with name:tree_value

## Upgradeable
Improvable (for 3.8+) syntaxes


### Unimport
`unimport` integration

- `db["community"]["unimport"]["unimport"]` => A list of imports that are not used
