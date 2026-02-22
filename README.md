# AVL Tree Library

A simple implementation of an AVL tree (self-balancing binary search tree). It stores values associated with keys and performs insertion, deletion, and search operations in $O(\log n)$ time.

## Installation

```bash
pip install BalancedBstAvl
```

## Usage

```python
from avltree import AVLTree

tree = AVLTree()
tree = tree.set(10, "a")
tree = tree.set(5, "b")
tree = tree.set(15, "c")

print(tree.find(10))
print(tree.get(5))
print(tree.items())

tree = tree.delete(10)
print(tree.items())
```

## Features

- Insert/Update keys: `set(x, value)` (inserts if not present, updates if exists)
- Delete keys: `delete(x)`
- Check key existence: `find(x)`
- Retrieve values: `get(x, default=None)`
- Traverse: `items()` (in ascending key order)

## Dependencies

- Runtime: None (Python standard library only)
- Development: `pytest` and others (install with `pip install -e .[dev]`)

## Supported Environments

- Python 3.9, 3.10, 3.11, 3.12, 3.13
- OS: Windows / macOS / Linux

## Development

```bash
pip install -e .[dev]
pytest
```

## License

MIT License
