"""
Minimal YAML subset parser (no external dependencies).

Supported:
- dicts with string keys
- lists
- scalars: strings, ints, floats, booleans, null

Not supported:
- anchors/aliases, multiline strings, complex quoting rules, tags, merges, etc.

This is intentionally strict: provider packs should remain within this subset so
validation is deterministic and CI doesn't need PyYAML.
"""

from __future__ import annotations

from dataclasses import dataclass


class YamlSubsetError(ValueError):
    pass


def _parse_scalar(raw: str):
    s = raw.strip()
    if s in ("null", "~"):
        return None
    if s in ("true", "True"):
        return True
    if s in ("false", "False"):
        return False
    # numbers
    try:
        if "." in s:
            return float(s)
        return int(s)
    except Exception:
        pass
    # strip simple quotes
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    return s


@dataclass
class _Line:
    indent: int
    text: str
    lineno: int


def load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        raw_lines = f.read().splitlines()

    lines: list[_Line] = []
    for idx, raw in enumerate(raw_lines, start=1):
        stripped = raw.rstrip()
        if not stripped or stripped.lstrip().startswith("#"):
            continue
        if "\t" in raw:
            raise YamlSubsetError(f"{path}:{idx}: tabs are not allowed")
        indent = len(raw) - len(raw.lstrip(" "))
        lines.append(_Line(indent=indent, text=raw.lstrip(" "), lineno=idx))

    i = 0

    def parse_block(expected_indent: int):
        nonlocal i
        # Decide container type by first token at expected indent.
        if i >= len(lines) or lines[i].indent < expected_indent:
            return None
        if lines[i].indent != expected_indent:
            raise YamlSubsetError(
                f"{path}:{lines[i].lineno}: expected indent {expected_indent}, got {lines[i].indent}"
            )
        if lines[i].text.startswith("- "):
            return parse_list(expected_indent)
        return parse_dict(expected_indent)

    def parse_list(expected_indent: int):
        nonlocal i
        out = []
        while i < len(lines) and lines[i].indent == expected_indent and lines[i].text.startswith("- "):
            item_text = lines[i].text[2:].strip()
            lineno = lines[i].lineno
            i += 1
            if item_text == "":
                # Nested block
                nested = parse_block(expected_indent + 2)
                if nested is None:
                    raise YamlSubsetError(f"{path}:{lineno}: list item cannot be empty")
                out.append(nested)
            elif ":" in item_text and not item_text.startswith(("'", '"')):
                # Support the common YAML pattern: "- key: value" with optional additional keys
                # on subsequent lines indented by +2.
                key, value = item_text.split(":", 1)
                key = key.strip()
                value = value.strip()
                if not key:
                    raise YamlSubsetError(f"{path}:{lineno}: empty key in inline mapping")
                item = {}
                if value == "":
                    nested = parse_block(expected_indent + 2)
                    if nested is None:
                        raise YamlSubsetError(f"{path}:{lineno}: empty value requires nested block")
                    item[key] = nested
                else:
                    item[key] = _parse_scalar(value)

                # Merge any additional key/value pairs for this list item.
                if i < len(lines) and lines[i].indent == expected_indent + 2 and not lines[i].text.startswith("- "):
                    extra = parse_dict(expected_indent + 2)
                    if not isinstance(extra, dict):
                        raise YamlSubsetError(f"{path}:{lines[i-1].lineno}: expected mapping block")
                    for k, v in extra.items():
                        if k in item:
                            raise YamlSubsetError(f"{path}:{lineno}: duplicate key in list item: {k}")
                        item[k] = v
                out.append(item)
            else:
                out.append(_parse_scalar(item_text))
        return out

    def parse_dict(expected_indent: int):
        nonlocal i
        out: dict[str, object] = {}
        while i < len(lines) and lines[i].indent == expected_indent and not lines[i].text.startswith("- "):
            raw = lines[i].text
            lineno = lines[i].lineno
            if ":" not in raw:
                raise YamlSubsetError(f"{path}:{lineno}: expected 'key: value'")
            key, value = raw.split(":", 1)
            key = key.strip()
            if not key:
                raise YamlSubsetError(f"{path}:{lineno}: empty key")
            value = value.strip()
            i += 1
            if value == "":
                nested = parse_block(expected_indent + 2)
                if nested is None:
                    # Allow explicit empty dict/list only via "{}" / "[]"
                    out[key] = None
                else:
                    out[key] = nested
            else:
                out[key] = _parse_scalar(value)
        return out

    doc = parse_block(0)
    if doc is None:
        return {}
    if i != len(lines):
        # Should be unreachable; means indentation went backwards unexpectedly.
        raise YamlSubsetError(f"{path}:{lines[i].lineno}: trailing content could not be parsed")
    return doc
