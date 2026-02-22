# AVL Tree Test Case Design Document

## Terminology

- **Rebalancing**: Adjustment operation (including rotations) performed when the AVL condition (height difference of subtrees exceeds acceptable range) is violated.
- **Successor**: The `in-order successor` used in deletion operations (the minimum node in the right subtree of the deletion target).

## 1. `__init__` (Constructor)

| No. | Test Aspect | Verification Content | Precondition | Test Procedure | Expected Result |
| --- | --- | --- | --- | --- | --- |
| 1-1 | `key` specification | None | - | `AVLTree()` | Internal attributes are `_key=None`, `_value=None`, `_h=0`, `_l=None`, `_r=None` |
| 1-2 | `key` specification | Present | - | `AVLTree(10)` | Internal attributes are `_key=10`, `_value=None`, `_h=1` |
| 2-1 | `value` specification | None | - | - | NN (verified in 1-2) |
| 2-2 | `value` specification | Present | - | `AVLTree(5, "val")` | Internal attributes are `_key=5`, `_value="val"`, `_h=1` |

## 2. `set(x: int, value: Any) → AVLTree`

| No. | Test Aspect | Verification Content | Precondition | Test Procedure | Expected Result |
| --- | --- | --- | --- | --- | --- |
| 1-1 | Root operation | Empty tree | `t = AVLTree()` | `t.set(5, "a")` | Can add a node to an empty tree. |
| 1-2 | Root operation | Update value | `t = AVLTree(); t.set(5, "old")` | `t.set(5, "new")` | Can update the root. |
| 2-1 | Left operation | Insert | `t = AVLTree(); t.set(10, "a")` | `t.set(5, "b")` | Can insert a node with key `5` and retrieve its value. |
| 2-2 | Left operation | Update value | `t = AVLTree(); t.set(10, "a"); set(5, "b")` | `set(5, "b_new")` | Value for key `5` can be updated. |
| 3-1 | Left-left operation | Insert (no rebalancing needed) | `t = AVLTree(); t.set(50, "a"); t.set(30, "b"); t.set(70, "c"); t.set(60, "d")` | `t.set(20, "f")` | Can insert a node to the left-left of root. No rebalancing occurs. |
| 3-2 | Left-left operation | Insert (rebalancing occurs) | `t = AVLTree(); t.set(10, "a"); t.set(5, "b")` | `t.set(3, "c")` | After inserting a node to the left-left of root, rebalancing occurs. |
| 3-3 | Left-left operation | Update value | `t = AVLTree(); t.set(50, "a"); t.set(30, "b"); t.set(70, "c"); t.set(60, "d"); t.set(20, "d")` | `t.set(20, "d_new")` | Value for key `20` can be updated. |
| 4-1 | Left-right operation | Insert (no rebalancing needed) | `t = AVLTree(); t.set(20, "a"); t.set(10, "b")` | `set(30, "c")` | Can insert a node to the left-right of root. No rebalancing occurs. |
| 4-2 | Left-right operation | Insert (rebalancing occurs) | `t = AVLTree(); t.set(10, "a"); t.set(3, "b")` | `t.set(5, "c")` | After inserting a node to the left-right of root, rebalancing occurs. |
| 4-3 | Left-right operation | Update value | `t = AVLTree(); t.set(20, "a"); t.set(10, "b"); t.set(30, "c")` | `t.set(30, "c_new")` | Value for key `30` can be updated. |
| 5-1 | Right operation | Insert | `t = AVLTree(); t.set(10, "a")` | `t.set(15, "b")` | Can insert a node with key `15` and retrieve its value. |
| 5-2 | Right operation | Update value | `t = AVLTree(); t.set(10, "a"); t.set(15, "b")` | `t.set(15, "b_new")` | Value for key `15` can be updated. |
| 6-1 | Right-left operation | Insert (no rebalancing needed) | `t = AVLTree(); t.set(20, "a"); t.set(10, "b"); t.set(40, "c")` | `t.set(35, "d")` | Can insert a node to the right-left of root. No rebalancing occurs. |
| 6-2 | Right-left operation | Insert (rebalancing occurs) | `t = AVLTree(); t.set(30, "a"); t.set(40, "b")` | `t.set(35, "c")` | Can insert a node to the right-left of root. Rebalancing occurs. |
| 6-3 | Right-left operation | Update value | `t = AVLTree(); t.set(10, "a"); t.set(30, "b"); t.set(20, "c")` | `set(20, "c_new")` | Value for key `20` can be updated. |
| 7-1 | Right-right operation | Insert (no rebalancing needed) | `t = AVLTree(); t.set(20, "a"); t.set(10, "b"); t.set(25, "c")` | `t.set(30, "d")` | Can insert a node to the right-right of root. No rebalancing occurs. |
| 7-2 | Right-right operation | Insert (rebalancing occurs) | `t = AVLTree(); t.set(30, "a"); t.set(40, "b")` | `t.set(50, "c")` | Can insert a node to the right-right of root. Rebalancing occurs. |
| 7-3 | Right-right operation | Update value | `t = AVLTree(); t.set(10, "a"); t.set(20, "b"); t.set(30, "c")` | `t.set(30, "c_new")` | Value for key `30` can be updated. |

## 3. `get(x: int, default=None) → Any`

| No. | Test Aspect | Precondition | Test Procedure | Expected Result |
| --- | --- | --- | --- | --- |
| 1-1 | Get from root (exists at root) | `t = AVLTree(); t.set(10, "a")` | `t.get(10)` | `"a"` |
| 1-2 | Get from root (not exists at root) | `t = AVLTree()` | `t.get(5)` | `None` |
| 2-1 | Get from left (exists on left) | `t = AVLTree(); t.set(10, "a"); t.set(5, "b")` | `t.get(5)` | `"b"` |
| 2-2 | Get from left (not exists on left) | `t = AVLTree(); t.set(10, "a"); t.set(5, "b")` | `t.get(3)` | `None` |
| 3-1 | Get from left-left (exists at left-left) | `t = AVLTree(); t.set(40, "a"); t.set(20, "b"); t.set(60, "c"); t.set(10, "d")` | `t.get(10)` | `"d"` |
| 3-2 | Get from left-left (not exists at left-left) | `t = AVLTree(); t.set(40, "a"); t.set(20, "b"); t.set(60, "c"); t.set(10, "d")` | `t.get(5)` | `None` |
| 4-1 | Get from left-right (exists at left-right) | `t = AVLTree(); t.set(40, "a"); t.set(20, "b"); t.set(60, "c"); t.set(10, "d"); t.set(30, "e")` | `t.get(30)` | `"e"` |
| 4-2 | Get from left-right (not exists at left-right) | `t = AVLTree(); t.set(40, "a"); t.set(20, "b"); t.set(60, "c"); t.set(10, "d"); t.set(30, "e")` | `t.get(15)` | `None` |
| 5-1 | Get from right (exists on right) | `t = AVLTree(); t.set(10, "a"); t.set(15, "b")` | `t.get(15)` | `"b"` |
| 5-2 | Get from right (not exists on right) | `t = AVLTree(); t.set(10, "a"); t.set(15, "b")` | `t.get(20)` | `None` |
| 6-1 | Get from right-left (exists at right-left) | `t = AVLTree(); t.set(20, "a"); t.set(40, "b"); t.set(10, "c"); t.set(30, "d"); t.set(50, "e")` | `t.get(30)` | `"d"` |
| 6-2 | Get from right-left (not exists at right-left) | `t = AVLTree(); t.set(20, "a"); t.set(40, "b"); t.set(10, "c"); t.set(30, "d"); t.set(50, "e")` | `t.get(25)` | `None` |
| 7-1 | Get from right-right (exists at right-right) | `t = AVLTree(); t.set(20, "a"); t.set(10, "b"); t.set(30, "c"); t.set(40, "d")` | `t.get(40)` | `"d"` |
| 7-2 | Get from right-right (not exists at right-right) | `t = AVLTree(); t.set(20, "a"); t.set(10, "b"); t.set(30, "c"); t.set(40, "d")` | `t.get(35)` | `None` |
| 8-1 | Default value specification (not specified) | `t = AVLTree()` | `t.get(5)` | `None` |
| 8-2 | Default value specification (specified) | `t = AVLTree()` | `t.get(5, "default")` | `"default"` |

## 4. `find(x: int) → bool`

| No. | Test Aspect | Precondition | Test Procedure | Expected Result |
| --- | --- | --- | --- | --- |
| 1-1 | Check root (exists at root) | `t = AVLTree(); t.set(10, "a")` | `t.find(10)` | Returns `True` |
| 1-2 | Check root (not exists at root) | `t = AVLTree()` | `t.find(5)` | Returns `False` |
| 2-1 | Check left (exists on left) | `t = AVLTree(); t.set(10, "a"); t.set(5, "b")` | `t.find(5)` | Returns `True` |
| 2-2 | Check left (not exists on left) | `t = AVLTree(); t.set(10, "a"); t.set(5, "b")` | `t.find(3)` | Returns `False` |
| 3-1 | Check left-left (exists at left-left) | `t = AVLTree(); t.set(40, "a"); t.set(20, "b"); t.set(60, "c"); t.set(10, "d")` | `t.find(10)` | Returns `True` |
| 3-2 | Check left-left (not exists at left-left) | `t = AVLTree(); t.set(40, "a"); t.set(20, "b"); t.set(60, "c"); t.set(10, "d")` | `t.find(5)` | Returns `False` |
| 4-1 | Check left-right (exists at left-right) | `t = AVLTree(); t.set(40, "a"); t.set(20, "b"); t.set(60, "c"); t.set(10, "d"); t.set(30, "e")` | `t.find(30)` | Returns `True` |
| 4-2 | Check left-right (not exists at left-right) | `t = AVLTree(); t.set(40, "a"); t.set(20, "b"); t.set(60, "c"); t.set(10, "d"); t.set(30, "e")` | `t.find(15)` | Returns `False` |
| 5-1 | Check right (exists on right) | `t = AVLTree(); t.set(10, "a"); t.set(15, "b")` | `t.find(15)` | Returns `True` |
| 5-2 | Check right (not exists on right) | `t = AVLTree(); t.set(10, "a"); t.set(15, "b")` | `t.find(20)` | Returns `False` |
| 6-1 | Check right-left (exists at right-left) | `t = AVLTree(); t.set(20, "a"); t.set(40, "b"); t.set(10, "c"); t.set(30, "d"); t.set(50, "e")` | `t.find(30)` | Returns `True` |
| 6-2 | Check right-left (not exists at right-left) | `t = AVLTree(); t.set(20, "a"); t.set(40, "b"); t.set(10, "c"); t.set(30, "d"); t.set(50, "e")` | `t.find(25)` | Returns `False` |
| 7-1 | Check right-right (exists at right-right) | `t = AVLTree(); t.set(20, "a"); t.set(10, "b"); t.set(30, "c"); t.set(40, "d")` | `t.find(40)` | Returns `True` |
| 7-2 | Check right-right (not exists at right-right) | `t = AVLTree(); t.set(20, "a"); t.set(10, "b"); t.set(30, "c"); t.set(40, "d")` | `t.find(35)` | Returns `False` |

## 5. `delete(x: int) → AVLTree`

| No. | Test Aspect | Precondition | Test Procedure | Expected Result |
| --- | --- | --- | --- | --- |
| 1-1 | Delete from root (no deletion/rebalancing needed) | `t = AVLTree(); t.set(10, "a"); t.set(5, "b")` | `t.delete(10)` | No rebalancing occurs and `items() == [(5, "b")]`. |
| 1-2 | Delete from root (rebalancing occurs) | `t = AVLTree(); t.set(40, "a"); t.set(20, "b"); t.set(60, "c"); t.set(10, "d"); t.set(5, "e")` | `t.delete(60)` | Rebalancing occurs after deletion and balance is preserved. |
| 1-3 | Delete from root (delete target not found) | `t = AVLTree()` | `t.delete(5)` | `items()` does not change. |
| 1-4 | Delete from root (root is a leaf) | `t = AVLTree(); t.set(5, "a")` | `t.delete(5)` | Tree becomes empty and `items() == []`. |
| 2-1 | Delete from left (no deletion/rebalancing needed) | `t = AVLTree(); t.set(30, "a"); t.set(10, "b"); t.set(40, "c")` | `t.delete(10)` | No rebalancing occurs and `items()` does not contain `10`. |
| 2-2 | Delete from left (rebalancing occurs) | `t = AVLTree(); t.set(50, "a"); t.set(30, "b"); t.set(70, "c"); t.set(20, "d"); t.set(10, "e")` | `t.delete(70)` | Rebalancing occurs after deletion and balance is preserved. |
| 2-3 | Delete from left (delete target not found) | `t = AVLTree(); t.set(30, "a"); t.set(10, "b")` | `t.delete(5)` | `items()` does not change. |
| 2-4 | Delete from left (delete non-leaf node) | `t = AVLTree(); t.set(50, "a"); t.set(30, "b"); t.set(20, "c"); t.set(40, "d")` | `t.delete(30)` | Node is deleted and `items()` is updated. |
| 3-1 | Delete from left-left (no deletion/rebalancing needed) | `t = AVLTree(); t.set(40, "a"); t.set(20, "b"); t.set(60, "c"); t.set(10, "d")` | `t.delete(10)` | No rebalancing occurs and `items()` does not contain `10`. |
| 3-2 | Delete from left-left (rebalancing occurs) | `t = AVLTree(); t.set(60, "a"); t.set(40, "b"); t.set(80, "c"); t.set(30, "d"); t.set(20, "e")` | `t.delete(80)` | Rebalancing occurs after deletion and balance is preserved. |
| 3-3 | Delete from left-left (delete target not found) | `t = AVLTree(); t.set(40, "a"); t.set(20, "b")` | `t.delete(5)` | `items()` does not change. |
| 4-1 | Delete from left-right (no deletion/rebalancing needed) | `t = AVLTree(); t.set(40, "a"); t.set(20, "b"); t.set(60, "c"); t.set(10, "d"); t.set(30, "e")` | `t.delete(30)` | No rebalancing occurs and `items()` does not contain `30`. |
| 4-2 | Delete from left-right (rebalancing occurs) | `t = AVLTree(); t.set(50, "a"); t.set(30, "b"); t.set(70, "c"); t.set(20, "d"); t.set(10, "e"); t.set(25, "f")` | `t.delete(70)` | Rebalancing occurs after deletion and balance is preserved. |
| 4-3 | Delete from left-right (delete target not found) | `t = AVLTree(); t.set(40, "a"); t.set(20, "b"); t.set(60, "c")` | `t.delete(15)` | `items()` does not change. |
| 5-1 | Delete from right (no deletion/rebalancing needed) | `t = AVLTree(); t.set(10, "a"); t.set(15, "b")` | `t.delete(15)` | No rebalancing occurs and `items() == [(10, "a")]`. |
| 5-2 | Delete from right (rebalancing occurs) | `t = AVLTree(); t.set(20, "a"); t.set(10, "b"); t.set(30, "c"); t.set(40, "d"); t.set(50, "e")` | `t.delete(10)` | Rebalancing occurs after deletion and balance is preserved. |
| 5-3 | Delete from right (delete target not found) | `t = AVLTree(); t.set(10, "a"); t.set(15, "b")` | `t.delete(20)` | `items()` does not change. |
| 5-4 | Delete from right (delete right node) | `t = AVLTree(); t.set(40, "a"); t.set(20, "b"); t.set(60, "c"); t.set(50, "d")` | `t.delete(50)` | Node is deleted and `items()` is updated. |
| 6-1 | Delete from right-left (no deletion/rebalancing needed) | `t = AVLTree(); t.set(20, "a"); t.set(40, "b"); t.set(10, "c"); t.set(30, "d"); t.set(50, "e")` | `t.delete(30)` | No rebalancing occurs and `items()` does not contain `30`. |
| 6-2 | Delete from right-left (rebalancing occurs) | `t = AVLTree(); t.set(30, "a"); t.set(10, "b"); t.set(50, "c"); t.set(5, "d"); t.set(15, "e"); t.set(12, "f")` | `t.delete(5)` | Rebalancing occurs after deletion and balance is preserved. |
| 6-3 | Delete from right-left (delete target not found) | `t = AVLTree(); t.set(20, "a"); t.set(40, "b"); t.set(10, "c")` | `t.delete(25)` | `items()` does not change. |
| 7-1 | Delete from right-right (no deletion/rebalancing needed) | `t = AVLTree(); t.set(20, "a"); t.set(10, "b"); t.set(30, "c"); t.set(40, "d")` | `t.delete(40)` | No rebalancing occurs and `items()` does not contain `40`. |
| 7-2 | Delete from right-right (rebalancing occurs) | `t = AVLTree(); t.set(10, "a"); t.set(20, "b"); t.set(30, "c"); t.set(40, "d"); t.set(50, "e")` | `t.delete(20)` | Rebalancing occurs after deletion and balance is preserved. |
| 7-3 | Delete from right-right (delete target not found) | `t = AVLTree(); t.set(20, "a"); t.set(10, "b"); t.set(30, "c")` | `t.delete(35)` | `items()` does not change. |
| 8-1 | Delete 2-child node (successor is leaf) | `t = AVLTree(); t.set(30, "a"); t.set(10, "b"); t.set(50, "c"); t.set(5, "d"); t.set(20, "e"); t.set(40, "f"); t.set(60, "g")` | `t.delete(30)` | `items()` does not contain `30`, `40` is replaced (sort order preserved), and no rebalancing occurs. |
| 8-2 | Delete 2-child node (successor has right child) | `t = AVLTree(); t.set(30, "a"); t.set(20, "b"); t.set(40, "c"); t.set(35, "d"); t.set(37, "e"); t.set(50, "f")` | `t.delete(30)` | `items()` does not contain `30`, `35` is replaced / `37` is moved appropriately (sort order preserved). |
| 8-3 | Delete 2-child node (rebalancing occurs after replacement) | `t = AVLTree(); t.set(50, "a"); t.set(30, "b"); t.set(70, "c"); t.set(20, "d"); t.set(40, "e"); t.set(60, "f"); t.set(80, "g"); t.set(10, "h"); t.set(5, "i"); t.set(25, "j"); t.set(35, "k"); t.set(45, "l")` | `t.delete(30)` | `items()` does not contain `30`, replaced by successor, rebalancing occurs after replacement, and AVL condition is preserved. |

## 6. `items() → list[tuple[int, Any]]`

| No. | Test Aspect | Precondition | Test Procedure | Expected Result |
| --- | --- | --- | --- | --- |
| 1-1 | Number of nodes: 0 (empty tree) | `t = AVLTree()` | `t.items()` | `[]` |
| 2-1 | Number of nodes: 1 (single node) | `t = AVLTree(); t.set(5, "a")` | `t.items()` | `[(5, "a")]` |
| 3-1 | Number of nodes: 2 (inserted in ascending order) | `t = AVLTree(); t.set(1, "a"); t.set(2, "b")` | `t.items()` | `[(1, "a"), (2, "b")]` |
| 3-2 | Number of nodes: 2 (inserted in descending order) | `t = AVLTree(); t.set(2, "a"); t.set(1, "b")` | `t.items()` | `[(1, "b"), (2, "a")]` |
| 4-1 | Number of nodes: 3 (inserted in ascending order) | `t = AVLTree(); t.set(1, "a"); t.set(2, "b"); t.set(3, "c")` | `t.items()` | `[(1, "a"), (2, "b"), (3, "c")]` |
| 4-2 | Number of nodes: 3 (inserted in descending order) | `t = AVLTree(); t.set(3, "a"); t.set(2, "b"); t.set(1, "c")` | `t.items()` | `[(1, "c"), (2, "b"), (3, "a")]` |
| 4-3 | Number of nodes: 3 (inserted in mixed order) | `t = AVLTree(); t.set(2, "a"); t.set(1, "b"); t.set(3, "c")` | `t.items()` | `[(1, "b"), (2, "a"), (3, "c")]` |
