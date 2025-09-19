import re
from typing import Any


_var_pattern = re.compile(r"\$\{([a-zA-Z_][a-zA-Z0-9_\.]*)\}")


def _lookup(ctx: dict[str, Any], path: str) -> Any:
    cur: Any = ctx
    for p in path.split("."):
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        else:
            return None
    return cur


def render_value(value: Any, ctx: dict[str, Any]) -> Any:
    if isinstance(value, str):
        def repl(m: re.Match[str]) -> str:
            key = m.group(1)
            v = _lookup(ctx, key)
            return "" if v is None else str(v)

        return _var_pattern.sub(repl, value)
    if isinstance(value, list):
        return [render_value(v, ctx) for v in value]
    if isinstance(value, dict):
        return {k: render_value(v, ctx) for k, v in value.items()}
    return value

