# Lict

A small Python toy project from February 2024 that combines dictionary lookup with a list of keys whose order can be edited explicitly.

The idea was to explore a container with both mapping and sequence operations: look up values by key, move keys to particular positions, slice ordered views, and sort entries by key or value. The original module mentions configuration management, ordered records, and ordered sets as possible uses.

This repository preserves an early personal experiment. The original implementation and exploratory helpers are kept for historical reference.

## How it works

`Lict` subclasses `dict` and maintains a separate list of keys. That list controls iteration and the order returned by `keys()`, `values()`, and `items()`. Python dictionaries already preserve insertion order; Lict explores making that order directly editable and accessible by position.

The main features are:

- Move or insert keys with `insert()`, reverse their order, and sort by keys or values.
- Find a key's position with `index()` and retrieve a key by position with `get()`.
- Slice `keys()`, `values()`, `items()`, and `copy()`.
- Accept mixed initialization inputs, including dictionaries, key/value pairs, sets, and bare keys.
- Assign a configurable `defval` to keys supplied without values.
- Reject duplicate keys in `append()` and `extend()`, while assignment and `update()` can replace existing values.

## Example

From the repository directory:

```python
from Lict import Lict

record = Lict([
    ("name", "Ada"),
    ("language", "Python"),
    "notes",  # A bare key receives defval, which defaults to None.
])

record.insert(0, "language")  # Move an existing key, keeping its value.
assert record.keys() == ["language", "name", "notes"]
assert record["language"] == "Python"
assert record.get(0) == "language"
assert record.items(slice(0, 2)) == [("language", "Python"), ("name", "Ada")]
assert record["notes"] is None

record.append("year", 2024)
assert record.remove(-1) == ("year", 2024)  # Remove by position.
```

All included files use only the Python standard library. Use Python 3.10 or newer to run the full set of helper scripts, which includes `match` statements. There is no packaging setup; the example imports the module directly.

## Files

| File | Purpose |
| --- | --- |
| [`Lict.py`](Lict.py) | Main container, with the original motivation and method documentation. |
| [`Lictier.py`](Lictier.py) | Experimental subclass exploring removal by slice. |
| [`Lict_kvgen_comp.py`](Lict_kvgen_comp.py) | Alternative key/value parsers using conditionals, exceptions, and pattern matching. |
| [`ArgsGen.py`](ArgsGen.py) | Random input generator used for experiments. |
| [`OrderedFMeta.py`](OrderedFMeta.py) | Small metaclass helper that collects callable attributes in definition order. |

## Reading the original API

Several methods intentionally differ from `dict`: `get(index)` returns a **key at a position**, the view methods return lists, and `pop()` / `remove()` return `(key, value)` pairs. `popitem()` is unsupported. Bare-key defaults are supplied when entries are created; they do not create entries on a missing-key lookup.

The source contains unfinished experiments and TODOs, and some operations (including the union operators) have implementation issues. Treat it as exploratory code rather than a maintained container library. For the original design notes, see the module docstring in [`Lict.py`](Lict.py).

The recorded Git history dates to 6–7 February 2024 (UTC). This README was added later to explain the project without changing that implementation.
