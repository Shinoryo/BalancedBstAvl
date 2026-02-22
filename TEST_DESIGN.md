# AVL Tree Test Case Design Document

## Terminology

- **Rebalancing**: Adjustment operation (including rotations) performed when the AVL condition (height difference of subtrees exceeds acceptable range) is violated.
- **Successor**: The `in-order successor` used in deletion operations (the minimum node in the right subtree of the deletion target).

## 1. `__init__` (Constructor)

| No. | Test Aspect | Verification Content | Precondition | Test Procedure | Expected Result |
| --- | --- | --- | --- | --- | --- |
| 1-1 | `key` specification | None | No precondition. | `AVLTree()` | Internal attributes are `_key=None`, `_value=None`, `_h=0`, `_l=None`, `_r=None` |
| 1-2 | `key` specification | Present | No precondition. | `AVLTree(10)` | Internal attributes are `_key=10`, `_value=None`, `_h=1` |
| 2-1 | `value` specification | None | No precondition. | - | NN (verified in 1-2) |
| 2-2 | `value` specification | Present | No precondition. | `AVLTree(5, "val")` | Internal attributes are `_key=5`, `_value="val"`, `_h=1` |

## 2. `set(x: int, value: Any) → AVLTree`

| No. | Test Aspect | Verification Content | Precondition | Test Procedure | Expected Result |
| --- | --- | --- | --- | --- | --- |
| 1-1 | Root operation | Empty tree | The tree is empty. | `t.set(5, "a")` | Can add a node to an empty tree. |
| 1-2 | Root operation | Update value | The tree has a root with key `5` and value `old`. | `t.set(5, "new")` | Can update the root. |
| 2-1 | Left operation | Insert | The tree has a root with key `10` and value `a`. | `t.set(5, "b")` | Can insert a node with key `5` and retrieve its value. |
| 2-2 | Left operation | Update value | The tree has keys `10` (root) and `5` (left child), with `5` mapped to `b`. | `set(5, "b_new")` | Value for key `5` can be updated. |
| 3-1 | Left-left operation | Insert (no rebalancing needed) | The tree has keys `50` (root), `30` (left), `70` (right), and `60` (right-left). | `t.set(20, "f")` | Can insert a node to the left-left of root. Balance is preserved. |
| 3-2 | Left-left operation | Insert (rebalancing occurs) | The tree has keys `10` (root) and `5` (left). | `t.set(3, "c")` | After inserting a node to the left-left of root, rebalancing occurs. |
| 3-3 | Left-left operation | Update value | The tree has keys `50`, `30`, `70`, `60`, and `20`, with `20` mapped to `d`. | `t.set(20, "d_new")` | Value for key `20` can be updated. |
| 4-1 | Left-right operation | Insert (no rebalancing needed) | The tree has keys `20` (root) and `10` (left). | `set(30, "c")` | Can insert a node to the left-right of root. Balance is preserved. |
| 4-2 | Left-right operation | Insert (rebalancing occurs) | The tree has keys `10` (root) and `3` (left). | `t.set(5, "c")` | After inserting a node to the left-right of root, rebalancing occurs. |
| 4-3 | Left-right operation | Update value | The tree has keys `20` (root), `10` (left), and `30` (right), with `30` mapped to `c`. | `t.set(30, "c_new")` | Value for key `30` can be updated. |
| 5-1 | Right operation | Insert | The tree has a root with key `10` and value `a`. | `t.set(15, "b")` | Can insert a node with key `15` and retrieve its value. |
| 5-2 | Right operation | Update value | The tree has keys `10` (root) and `15` (right), with `15` mapped to `b`. | `t.set(15, "b_new")` | Value for key `15` can be updated. |
| 6-1 | Right-left operation | Insert (no rebalancing needed) | The tree has keys `20` (root), `10` (left), and `40` (right). | `t.set(35, "d")` | Can insert a node to the right-left of root. Balance is preserved. |
| 6-2 | Right-left operation | Insert (rebalancing occurs) | The tree has keys `30` (root) and `40` (right). | `t.set(35, "c")` | Can insert a node to the right-left of root. Rebalancing occurs. |
| 6-3 | Right-left operation | Update value | The tree has keys `10` (root), `30` (right), and `20` (right-left), with `20` mapped to `c`. | `set(20, "c_new")` | Value for key `20` can be updated. |
| 7-1 | Right-right operation | Insert (no rebalancing needed) | The tree has keys `20` (root), `10` (left), and `25` (right). | `t.set(30, "d")` | Can insert a node to the right-right of root. Balance is preserved. |
| 7-2 | Right-right operation | Insert (rebalancing occurs) | The tree has keys `30` (root) and `40` (right). | `t.set(50, "c")` | Can insert a node to the right-right of root. Rebalancing occurs. |
| 7-3 | Right-right operation | Update value | The tree has keys `10` (root), `20` (right), and `30` (right-right), with `30` mapped to `c`. | `t.set(30, "c_new")` | Value for key `30` can be updated. |

## 3. `get(x: int, default=None) → Any`

| No. | Test Aspect | Precondition | Test Procedure | Expected Result |
| --- | --- | --- | --- | --- |
| 1-1 | Get from root (exists at root) | The tree has a root with key `10` and value `a`. | `t.get(10)` | `"a"` |
| 1-2 | Get from root (not exists at root) | The tree is empty. | `t.get(5)` | `None` |
| 2-1 | Get from left (exists on left) | The tree has keys `10` (root) and `5` (left), with `5` mapped to `b`. | `t.get(5)` | `"b"` |
| 2-2 | Get from left (not exists on left) | The tree has keys `10` (root) and `5` (left). | `t.get(3)` | `None` |
| 3-1 | Get from left-left (exists at left-left) | The tree has keys `40` (root), `20` (left), `60` (right), and `10` (left-left), with `10` mapped to `d`. | `t.get(10)` | `"d"` |
| 3-2 | Get from left-left (not exists at left-left) | The tree has keys `40` (root), `20` (left), `60` (right), and `10` (left-left). | `t.get(5)` | `None` |
| 4-1 | Get from left-right (exists at left-right) | The tree has keys `40` (root), `20` (left), `60` (right), `10` (left-left), and `30` (left-right), with `30` mapped to `e`. | `t.get(30)` | `"e"` |
| 4-2 | Get from left-right (not exists at left-right) | The tree has keys `40` (root), `20` (left), `60` (right), `10` (left-left), and `30` (left-right). | `t.get(15)` | `None` |
| 5-1 | Get from right (exists on right) | The tree has keys `10` (root) and `15` (right), with `15` mapped to `b`. | `t.get(15)` | `"b"` |
| 5-2 | Get from right (not exists on right) | The tree has keys `10` (root) and `15` (right). | `t.get(20)` | `None` |
| 6-1 | Get from right-left (exists at right-left) | The tree has keys `20` (root), `10` (left), `40` (right), `30` (right-left), and `50` (right-right), with `30` mapped to `d`. | `t.get(30)` | `"d"` |
| 6-2 | Get from right-left (not exists at right-left) | The tree has keys `20` (root), `10` (left), `40` (right), `30` (right-left), and `50` (right-right). | `t.get(25)` | `None` |
| 7-1 | Get from right-right (exists at right-right) | The tree has keys `20` (root), `10` (left), `30` (right), and `40` (right-right), with `40` mapped to `d`. | `t.get(40)` | `"d"` |
| 7-2 | Get from right-right (not exists at right-right) | The tree has keys `20` (root), `10` (left), `30` (right), and `40` (right-right). | `t.get(35)` | `None` |
| 8-1 | Default value specification (not specified) | The tree is empty. | `t.get(5)` | `None` |
| 8-2 | Default value specification (specified) | The tree is empty. | `t.get(5, "default")` | `"default"` |

## 4. `find(x: int) → bool`

| No. | Test Aspect | Precondition | Test Procedure | Expected Result |
| --- | --- | --- | --- | --- |
| 1-1 | Check root (exists at root) | The tree has a root with key `10` and value `a`. | `t.find(10)` | Returns `True` |
| 1-2 | Check root (not exists at root) | The tree is empty. | `t.find(5)` | Returns `False` |
| 2-1 | Check left (exists on left) | The tree has keys `10` (root) and `5` (left). | `t.find(5)` | Returns `True` |
| 2-2 | Check left (not exists on left) | The tree has keys `10` (root) and `5` (left). | `t.find(3)` | Returns `False` |
| 3-1 | Check left-left (exists at left-left) | The tree has keys `40` (root), `20` (left), `60` (right), and `10` (left-left). | `t.find(10)` | Returns `True` |
| 3-2 | Check left-left (not exists at left-left) | The tree has keys `40` (root), `20` (left), `60` (right), and `10` (left-left). | `t.find(5)` | Returns `False` |
| 4-1 | Check left-right (exists at left-right) | The tree has keys `40` (root), `20` (left), `60` (right), `10` (left-left), and `30` (left-right). | `t.find(30)` | Returns `True` |
| 4-2 | Check left-right (not exists at left-right) | The tree has keys `40` (root), `20` (left), `60` (right), `10` (left-left), and `30` (left-right). | `t.find(15)` | Returns `False` |
| 5-1 | Check right (exists on right) | The tree has keys `10` (root) and `15` (right). | `t.find(15)` | Returns `True` |
| 5-2 | Check right (not exists on right) | The tree has keys `10` (root) and `15` (right). | `t.find(20)` | Returns `False` |
| 6-1 | Check right-left (exists at right-left) | The tree has keys `20` (root), `10` (left), `40` (right), `30` (right-left), and `50` (right-right). | `t.find(30)` | Returns `True` |
| 6-2 | Check right-left (not exists at right-left) | The tree has keys `20` (root), `10` (left), `40` (right), `30` (right-left), and `50` (right-right). | `t.find(25)` | Returns `False` |
| 7-1 | Check right-right (exists at right-right) | The tree has keys `20` (root), `10` (left), `30` (right), and `40` (right-right). | `t.find(40)` | Returns `True` |
| 7-2 | Check right-right (not exists at right-right) | The tree has keys `20` (root), `10` (left), `30` (right), and `40` (right-right). | `t.find(35)` | Returns `False` |

## 5. `delete(x: int) → AVLTree`

| No. | Test Aspect | Precondition | Test Procedure | Expected Result |
| --- | --- | --- | --- | --- |
| 1-1 | Delete from root (no deletion/rebalancing needed) | The tree has keys `10` (root) and `5` (left). | `t.delete(10)` | Deleted key is removed and balance is preserved. |
| 1-2 | Delete from root (rebalancing occurs) | The tree has keys `40` (root), `20` (left), `60` (right), `10` (left-left), and `5` (left-left-left). | `t.delete(60)` | Rebalancing occurs after deletion and balance is preserved. |
| 1-3 | Delete from root (delete target not found) | The tree is empty. | `t.delete(5)` | Tree remains unchanged and balance is preserved. |
| 1-4 | Delete from root (root is a leaf) | The tree has only a root with key `5`. | `t.delete(5)` | Tree becomes empty and balance is preserved. |
| 2-1 | Delete from left (no deletion/rebalancing needed) | The tree has keys `30` (root), `10` (left), and `40` (right). | `t.delete(10)` | Deleted key is removed and balance is preserved. |
| 2-2 | Delete from left (rebalancing occurs) | The tree has keys `50` (root), `30` (left), `70` (right), `20` (left-left), and `10` (left-left-left). | `t.delete(70)` | Rebalancing occurs after deletion and balance is preserved. |
| 2-3 | Delete from left (delete target not found) | The tree has keys `30` (root) and `10` (left). | `t.delete(5)` | Tree remains unchanged and balance is preserved. |
| 2-4 | Delete from left (delete non-leaf node) | The tree has keys `50` (root), `30` (left), `20` (left-left), and `40` (left-right). | `t.delete(30)` | Deleted key is removed and balance is preserved. |
| 3-1 | Delete from left-left (no deletion/rebalancing needed) | The tree has keys `40` (root), `20` (left), `60` (right), and `10` (left-left). | `t.delete(10)` | Deleted key is removed and balance is preserved. |
| 3-2 | Delete from left-left (rebalancing occurs) | The tree has keys `60` (root), `40` (left), `80` (right), `30` (left-left), and `20` (left-left-left). | `t.delete(80)` | Rebalancing occurs after deletion and balance is preserved. |
| 3-3 | Delete from left-left (delete target not found) | The tree has keys `40` (root) and `20` (left). | `t.delete(5)` | Tree remains unchanged and balance is preserved. |
| 4-1 | Delete from left-right (no deletion/rebalancing needed) | The tree has keys `40` (root), `20` (left), `60` (right), `10` (left-left), and `30` (left-right). | `t.delete(30)` | Deleted key is removed and balance is preserved. |
| 4-2 | Delete from left-right (rebalancing occurs) | The tree has keys `50` (root), `30` (left), `70` (right), `20` (left-left), `10` (left-left-left), and `25` (left-right). | `t.delete(70)` | Rebalancing occurs after deletion and balance is preserved. |
| 4-3 | Delete from left-right (delete target not found) | The tree has keys `40` (root), `20` (left), and `60` (right). | `t.delete(15)` | Tree remains unchanged and balance is preserved. |
| 5-1 | Delete from right (no deletion/rebalancing needed) | The tree has keys `10` (root) and `15` (right). | `t.delete(15)` | Deleted key is removed and balance is preserved. |
| 5-2 | Delete from right (rebalancing occurs) | The tree has keys `20` (root), `10` (left), `30` (right), `40` (right-right), and `50` (right-right-right). | `t.delete(10)` | Rebalancing occurs after deletion and balance is preserved. |
| 5-3 | Delete from right (delete target not found) | The tree has keys `10` (root) and `15` (right). | `t.delete(20)` | Tree remains unchanged and balance is preserved. |
| 5-4 | Delete from right (delete right node) | The tree has keys `40` (root), `20` (left), `60` (right), and `50` (right-left). | `t.delete(50)` | Deleted key is removed and balance is preserved. |
| 6-1 | Delete from right-left (no deletion/rebalancing needed) | The tree has keys `20` (root), `40` (right), `10` (left), `30` (right-left), and `50` (right-right). | `t.delete(30)` | Deleted key is removed and balance is preserved. |
| 6-2 | Delete from right-left (rebalancing occurs) | The tree has keys `30` (root), `10` (left), `50` (right), `5` (left-left), `15` (left-right), and `12` (left-right-left). | `t.delete(5)` | Rebalancing occurs after deletion and balance is preserved. |
| 6-3 | Delete from right-left (delete target not found) | The tree has keys `20` (root), `40` (right), and `10` (left). | `t.delete(25)` | Tree remains unchanged and balance is preserved. |
| 7-1 | Delete from right-right (no deletion/rebalancing needed) | The tree has keys `20` (root), `10` (left), `30` (right), and `40` (right-right). | `t.delete(40)` | Deleted key is removed and balance is preserved. |
| 7-2 | Delete from right-right (rebalancing occurs) | The tree has keys `10` (root), `20` (right), `30` (right-right), `40` (right-right-right), and `50` (right-right-right-right). | `t.delete(20)` | Rebalancing occurs after deletion and balance is preserved. |
| 7-3 | Delete from right-right (delete target not found) | The tree has keys `20` (root), `10` (left), and `30` (right). | `t.delete(35)` | Tree remains unchanged and balance is preserved. |
| 8-1 | Delete 2-child node (successor is leaf) | The tree has keys `30` (root), `10` (left), `50` (right), `5` (left-left), `20` (left-right), `40` (right-left), and `60` (right-right). | `t.delete(30)` | Deleted key is removed, successor replacement occurs, and balance is preserved. |
| 8-2 | Delete 2-child node (successor has right child) | The tree has keys `30` (root), `20` (left), `40` (right), `35` (right-left), `37` (right-left-right), and `50` (right-right). | `t.delete(30)` | Deleted key is removed, successor replacement occurs, and balance is preserved. |
| 8-3 | Delete 2-child node (rebalancing occurs after replacement) | The tree has keys `50` (root), `30` (left), `70` (right), `20` (left-left), `40` (left-right), `60` (right-left), `80` (right-right), `10` (left-left-left), `5` (left-left-left-left), `25` (left-left-right), `35` (left-right-left), and `45` (left-right-right). | `t.delete(30)` | Deleted key is removed, successor replacement occurs, and balance is preserved. |

## 6. `items() → list[tuple[int, Any]]`

| No. | Test Aspect | Precondition | Test Procedure | Expected Result |
| --- | --- | --- | --- | --- |
| 1-1 | Number of nodes: 0 (empty tree) | The tree is empty. | `t.items()` | `[]` |
| 2-1 | Number of nodes: 1 (single node) | The tree has a single node with key `5` and value `a`. | `t.items()` | `[(5, "a")]` |
| 3-1 | Number of nodes: 2 (inserted in ascending order) | The tree has two nodes with keys `1` and `2`, linked so that `2` is the right child of `1`. | `t.items()` | `[(1, "a"), (2, "b")]` |
| 3-2 | Number of nodes: 2 (inserted in descending order) | The tree has two nodes with keys `2` and `1`, linked so that `1` is the left child of `2`. | `t.items()` | `[(1, "b"), (2, "a")]` |
| 4-1 | Number of nodes: 3 (inserted in ascending order) | The tree has three nodes with keys `1`, `2`, and `3`, linked in a right-leaning chain. | `t.items()` | `[(1, "a"), (2, "b"), (3, "c")]` |
| 4-2 | Number of nodes: 3 (inserted in descending order) | The tree has three nodes with keys `3`, `2`, and `1`, linked in a left-leaning chain. | `t.items()` | `[(1, "c"), (2, "b"), (3, "a")]` |
| 4-3 | Number of nodes: 3 (inserted in mixed order) | The tree has three nodes with keys `2` (root), `1` (left), and `3` (right). | `t.items()` | `[(1, "b"), (2, "a"), (3, "c")]` |
