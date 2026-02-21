# AVL Tree Library

AVL木（自己平衡二分探索木）のシンプルな実装です。キーに付随する値を保持でき、挿入・削除・検索を $O(\log n)$ で行います。

## インストール

```bash
pip install avltree
```

## 使い方

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

## 機能

- キーの挿入/更新: `set(x, value)` (存在しない場合は挿入、存在する場合は更新)
- キーの削除: `delete(x)`
- キーの存在確認: `find(x)`
- 値の取得: `get(x, default=None)`
- 走査: `items()` (キー昇順)

## 開発

```bash
pip install -e .[dev]
pytest
```

## ライセンス

MIT License
