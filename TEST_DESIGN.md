# AVL Tree Test Case Design Document

## Overview

All test cases verify both **correctness of operations** and **height consistency**. According to the AVL tree definition, the height of each node must satisfy:

- Empty node: `_h = 0`
- Non-empty node: `_h = 1 + max(height(left_child), height(right_child))`

This property is validated in every test through the `_assert_height_consistency()` helper function.

## Terminology

- **Rebalancing**: Adjustment operation (including rotations) performed when the AVL condition (height difference of subtrees exceeds acceptable range) is violated.
- **Successor**: The `in-order successor` used in deletion operations (the minimum node in the right subtree of the deletion target).
- **Height (`_h`)**: The height of a node is defined as:
  - `0` if the node is empty (key is None)
  - `1 + max(height(left_child), height(right_child))` for non-empty nodes
  - Must be correctly updated after insertions, deletions, and rotations

## 1. `__init__` (Constructor)

| No. | Test Aspect | Verification Content | Precondition | Test Procedure | Expected Result |
| --- | --- | --- | --- | --- | --- |
| 1-1 | `key` specification | None | No precondition. | `AVLTree()` | Internal attributes are `_key=None`, `_value=None`, `_h=0`, `_l=None`, `_r=None` |
| 1-2 | `key` specification | Present | No precondition. | `AVLTree(0)` | Internal attributes are `_key=0`, `_value=None`, `_h=1` |
| 2-1 | `value` specification | None | No precondition. | - | NN (verified in 1-2) |
| 2-2 | `value` specification | Present | No precondition. | `AVLTree(-5, "val")` | Internal attributes are `_key=-5`, `_value="val"`, `_h=1` |

## 2. `set(x: int, value: Any) → AVLTree`

| No. | Test Aspect | Verification Content | Precondition | Test Procedure | Expected Result |
| --- | --- | --- | --- | --- | --- |
| 1-1 | Set to empty tree | Node insertion in empty tree | The tree is empty. | `t.set(0, "a")` | Can add a node to an empty tree. |
| 1-2 | Set update root | Value update on root | The tree has a root with key `0` and value `old`. | `t.set(0, "new")` | Can update the root. |
| 2-1 | Set insert left | Node insertion to left of root | The tree has a root with key `10` and value `a`. | `t.set(-5, "b")` | Can insert a node with key `-5` and retrieve its value. |
| 2-2 | Set update left | Value update on left child | The tree has keys `10` (root) and `-5` (left child), with `-5` mapped to `b`. | `t.set(-5, "b_new")` | Value for key `-5` can be updated. |
| 3-1 | Set insert left-left (no rebalance) | Node insertion to left-left without rebalancing | The tree has keys `50` (root), `30` (left), `70` (right), and `60` (right-left). | `t.set(-20, "f")` | Can insert a node to the left-left of root. Balance is preserved. |
| 3-2 | Set insert left-left (with rebalance) | Node insertion to left-left with rebalancing | The tree has keys `10` (root) and `-5` (left). | `t.set(-15, "c")` | After inserting a node to the left-left of root, rebalancing occurs. |
| 3-3 | Set update left-left | Value update on left-left node | The tree has keys `50`, `30`, `70`, `60`, and `-20`, with `-20` mapped to `d`. | `t.set(-20, "d_new")` | Value for key `-20` can be updated. |
| 4-1 | Set insert left-right (no rebalance) | Node insertion to left-right without rebalancing | The tree has keys `20` (root) and `-10` (left). | `t.set(30, "c")` | Can insert a node to the left-right of root. Balance is preserved. |
| 4-2 | Set insert left-right (with rebalance) | Node insertion to left-right with rebalancing | The tree has keys `10` (root) and `-15` (left). | `t.set(-5, "c")` | After inserting a node to the left-right of root, rebalancing occurs. |
| 4-3 | Set update left-right | Value update on left-right node | The tree has keys `20` (root), `10` (left), and `30` (right), with `30` mapped to `c`. | `t.set(30, "c_new")` | Value for key `30` can be updated. |
| 5-1 | Set insert right | Node insertion to right of root | The tree has a root with key `10` and value `a`. | `t.set(15, "b")` | Can insert a node with key `15` and retrieve its value. |
| 5-2 | Set update right | Value update on right child | The tree has keys `10` (root) and `15` (right), with `15` mapped to `b`. | `t.set(15, "b_new")` | Value for key `15` can be updated. |
| 6-1 | Set insert right-left (no rebalance) | Node insertion to right-left without rebalancing | The tree has keys `20` (root), `10` (left), and `40` (right). | `t.set(35, "d")` | Can insert a node to the right-left of root. Balance is preserved. |
| 6-2 | Set insert right-left (with rebalance) | Node insertion to right-left with rebalancing | The tree has keys `30` (root) and `40` (right). | `t.set(35, "c")` | Can insert a node to the right-left of root. Rebalancing occurs. |
| 6-3 | Set update right-left | Value update on right-left node | The tree has keys `10` (root), `30` (right), and `20` (right-left), with `20` mapped to `c`. | `t.set(20, "c_new")` | Value for key `20` can be updated. |
| 7-1 | Set insert right-right (no rebalance) | Node insertion to right-right without rebalancing | The tree has keys `20` (root), `10` (left), and `25` (right). | `t.set(30, "d")` | Can insert a node to the right-right of root. Balance is preserved. |
| 7-2 | Set insert right-right (with rebalance) | Node insertion to right-right with rebalancing | The tree has keys `30` (root) and `40` (right). | `t.set(50, "c")` | Can insert a node to the right-right of root. Rebalancing occurs. |
| 7-3 | Set update right-right | Value update on right-right node | The tree has keys `10` (root), `20` (right), and `30` (right-right), with `30` mapped to `c`. | `t.set(30, "c_new")` | Value for key `30` can be updated. |

## 3. `get(x: int, default=None) → Any`

| No. | Test Aspect | Precondition | Test Procedure | Expected Result |
| --- | --- | --- | --- | --- |
| 1-1 | Get from root (found) | The tree has a root with key `0` and value `a`. | `t.get(0)` | `"a"` |
| 1-2 | Get from root (not found) | The tree is empty. | `t.get(5)` | `None` |
| 2-1 | Get from left (found) | The tree has keys `10` (root) and `-5` (left), with `-5` mapped to `b`. | `t.get(-5)` | `"b"` |
| 2-2 | Get from left (not found) | The tree has keys `10` (root) and `-5` (left). | `t.get(-15)` | `None` |
| 3-1 | Get from left-left (found) | The tree has keys `40` (root), `20` (left), `60` (right), and `-10` (left-left), with `-10` mapped to `d`. | `t.get(-10)` | `"d"` |
| 3-2 | Get from left-left (not found) | The tree has keys `40` (root), `20` (left), `60` (right), and `-10` (left-left). | `t.get(-25)` | `None` |
| 4-1 | Get from left-right (found) | The tree has keys `40` (root), `20` (left), `60` (right), `10` (left-left), and `30` (left-right), with `30` mapped to `e`. | `t.get(30)` | `"e"` |
| 4-2 | Get from left-right (not found) | The tree has keys `40` (root), `20` (left), `60` (right), `10` (left-left), and `30` (left-right). | `t.get(15)` | `None` |
| 5-1 | Get from right (found) | The tree has keys `0` (root) and `15` (right), with `15` mapped to `b`. | `t.get(15)` | `"b"` |
| 5-2 | Get from right (not found) | The tree has keys `0` (root) and `15` (right). | `t.get(20)` | `None` |
| 6-1 | Get from right-left (found) | The tree has keys `20` (root), `10` (left), `40` (right), `30` (right-left), and `50` (right-right), with `30` mapped to `d`. | `t.get(30)` | `"d"` |
| 6-2 | Get from right-left (not found) | The tree has keys `20` (root), `10` (left), `40` (right), `30` (right-left), and `50` (right-right). | `t.get(25)` | `None` |
| 7-1 | Get from right-right (found) | The tree has keys `20` (root), `10` (left), `30` (right), and `40` (right-right), with `40` mapped to `d`. | `t.get(40)` | `"d"` |
| 7-2 | Get from right-right (not found) | The tree has keys `20` (root), `10` (left), `30` (right), and `40` (right-right). | `t.get(35)` | `None` |
| 8-1 | Get with default (not specified) | The tree is empty. | `t.get(5)` | `None` |
| 8-2 | Get with default (specified) | The tree is empty. | `t.get(5, "default")` | `"default"` |

## 4. `find(x: int) → bool`

| No. | Test Aspect | Precondition | Test Procedure | Expected Result |
| --- | --- | --- | --- | --- |
| 1-1 | Find root (found) | The tree has a root with key `0` and value `a`. | `t.find(0)` | Returns `True` |
| 1-2 | Find root (not found) | The tree is empty. | `t.find(5)` | Returns `False` |
| 2-1 | Find left (found) | The tree has keys `10` (root) and `-5` (left). | `t.find(-5)` | Returns `True` |
| 2-2 | Find left (not found) | The tree has keys `10` (root) and `-5` (left). | `t.find(-15)` | Returns `False` |
| 3-1 | Find left-left (found) | The tree has keys `40` (root), `20` (left), `60` (right), and `-10` (left-left). | `t.find(-10)` | Returns `True` |
| 3-2 | Find left-left (not found) | The tree has keys `40` (root), `20` (left), `60` (right), and `-10` (left-left). | `t.find(-25)` | Returns `False` |
| 4-1 | Find left-right (found) | The tree has keys `40` (root), `20` (left), `60` (right), `10` (left-left), and `30` (left-right). | `t.find(30)` | Returns `True` |
| 4-2 | Find left-right (not found) | The tree has keys `40` (root), `20` (left), `60` (right), `10` (left-left), and `30` (left-right). | `t.find(15)` | Returns `False` |
| 5-1 | Find right (found) | The tree has keys `0` (root) and `15` (right). | `t.find(15)` | Returns `True` |
| 5-2 | Find right (not found) | The tree has keys `0` (root) and `15` (right). | `t.find(20)` | Returns `False` |
| 6-1 | Find right-left (found) | The tree has keys `20` (root), `10` (left), `40` (right), `30` (right-left), and `50` (right-right). | `t.find(30)` | Returns `True` |
| 6-2 | Find right-left (not found) | The tree has keys `20` (root), `10` (left), `40` (right), `30` (right-left), and `50` (right-right). | `t.find(25)` | Returns `False` |
| 7-1 | Find right-right (found) | The tree has keys `20` (root), `10` (left), `30` (right), and `40` (right-right). | `t.find(40)` | Returns `True` |
| 7-2 | Find right-right (not found) | The tree has keys `20` (root), `10` (left), `30` (right), and `40` (right-right). | `t.find(35)` | Returns `False` |

## 5. `delete(x: int) → AVLTree`

| No. | Test Aspect | Precondition | Test Procedure | Expected Result |
| --- | --- | --- | --- | --- |
| 1-1 | Delete from root (no rebalance) | The tree has keys `10` (root) and `5` (left). | `t.delete(10)` | Deleted key is removed and balance is preserved. |
| 1-2 | Delete from root (with rebalance) | The tree has keys `40` (root), `20` (left), `60` (right), `10` (left-left), and `5` (left-left-left). | `t.delete(60)` | Rebalancing occurs after deletion and balance is preserved. |
| 1-3 | Delete from root (not found) | The tree is empty. | `t.delete(5)` | Tree remains unchanged and balance is preserved. |
| 1-4 | Delete from root (leaf) | The tree has only a root with key `5`. | `t.delete(5)` | Tree becomes empty and balance is preserved. |
| 2-1 | Delete from left (no rebalance) | The tree has keys `30` (root), `-10` (left), and `40` (right). | `t.delete(-10)` | Deleted key is removed and balance is preserved. |
| 2-2 | Delete from left (with rebalance) | The tree has keys `50` (root), `30` (left), `70` (right), `20` (left-left), and `10` (left-left-left). | `t.delete(70)` | Rebalancing occurs after deletion and balance is preserved. |
| 2-3 | Delete from left (not found) | The tree has keys `30` (root) and `-10` (left). | `t.delete(-5)` | Tree remains unchanged and balance is preserved. |
| 2-4 | Delete from left (with children) | The tree has keys `50` (root), `30` (left), `-20` (left-left), and `40` (left-right). | `t.delete(30)` | Deleted key is removed and balance is preserved. |
| 3-1 | Delete from left-left (no rebalance) | The tree has keys `40` (root), `20` (left), `60` (right), and `10` (left-left). | `t.delete(10)` | Deleted key is removed and balance is preserved. |
| 3-2 | Delete from left-left (with rebalance) | The tree has keys `60` (root), `40` (left), `80` (right), `30` (left-left), and `20` (left-left-left). | `t.delete(80)` | Rebalancing occurs after deletion and balance is preserved. |
| 3-3 | Delete from left-left (not found) | The tree has keys `40` (root) and `20` (left). | `t.delete(5)` | Tree remains unchanged and balance is preserved. |
| 4-1 | Delete from left-right (no rebalance) | The tree has keys `40` (root), `20` (left), `60` (right), `10` (left-left), and `30` (left-right). | `t.delete(30)` | Deleted key is removed and balance is preserved. |
| 4-2 | Delete from left-right (with rebalance) | The tree has keys `50` (root), `30` (left), `70` (right), `20` (left-left), `10` (left-left-left), and `25` (left-right). | `t.delete(70)` | Rebalancing occurs after deletion and balance is preserved. |
| 4-3 | Delete from left-right (not found) | The tree has keys `40` (root), `20` (left), and `60` (right). | `t.delete(15)` | Tree remains unchanged and balance is preserved. |
| 5-1 | Delete from right (no rebalance) | The tree has keys `0` (root) and `15` (right). | `t.delete(15)` | Deleted key is removed and balance is preserved. |
| 5-2 | Delete from right (with rebalance) | The tree has keys `20` (root), `10` (left), `30` (right), `40` (right-right), and `50` (right-right-right). | `t.delete(10)` | Rebalancing occurs after deletion and balance is preserved. |
| 5-3 | Delete from right (not found) | The tree has keys `10` (root) and `15` (right). | `t.delete(20)` | Tree remains unchanged and balance is preserved. |
| 5-4 | Delete from right (with children) | The tree has keys `40` (root), `20` (left), `60` (right), and `50` (right-left). | `t.delete(50)` | Deleted key is removed and balance is preserved. |
| 6-1 | Delete from right-left (no rebalance) | The tree has keys `20` (root), `40` (right), `10` (left), `30` (right-left), and `50` (right-right). | `t.delete(30)` | Deleted key is removed and balance is preserved. |
| 6-2 | Delete from right-left (with rebalance) | The tree has keys `30` (root), `10` (left), `50` (right), `5` (left-left), `15` (left-right), and `12` (left-right-left). | `t.delete(5)` | Rebalancing occurs after deletion and balance is preserved. |
| 6-3 | Delete from right-left (not found) | The tree has keys `20` (root), `40` (right), and `10` (left). | `t.delete(25)` | Tree remains unchanged and balance is preserved. |
| 7-1 | Delete from right-right (no rebalance) | The tree has keys `20` (root), `10` (left), `30` (right), and `40` (right-right). | `t.delete(40)` | Deleted key is removed and balance is preserved. |
| 7-2 | Delete from right-right (with rebalance) | The tree has keys `10` (root), `20` (right), `30` (right-right), `40` (right-right-right), and `50` (right-right-right-right). | `t.delete(20)` | Rebalancing occurs after deletion and balance is preserved. |
| 7-3 | Delete from right-right (not found) | The tree has keys `20` (root), `10` (left), and `30` (right). | `t.delete(35)` | Tree remains unchanged and balance is preserved. |
| 8-1 | Delete 2-child (successor is leaf) | The tree has keys `30` (root), `10` (left), `50` (right), `5` (left-left), `20` (left-right), `40` (right-left), and `60` (right-right). | `t.delete(30)` | Deleted key is removed, successor replacement occurs, and balance is preserved. |
| 8-2 | Delete 2-child (successor has right child) | The tree has keys `30` (root), `20` (left), `40` (right), `35` (right-left), `37` (right-left-right), and `50` (right-right). | `t.delete(30)` | Deleted key is removed, successor replacement occurs, and balance is preserved. |
| 8-3 | Delete 2-child (with rebalance) | The tree has keys `50` (root), `30` (left), `70` (right), `20` (left-left), `40` (left-right), `60` (right-left), `80` (right-right), `10` (left-left-left), `5` (left-left-left-left), `25` (left-left-right), `35` (left-right-left), and `45` (left-right-right). | `t.delete(30)` | Deleted key is removed, successor replacement occurs, and balance is preserved. |

## 6. `items() → list[tuple[int, Any]]`

| No. | Test Aspect | Precondition | Test Procedure | Expected Result |
| --- | --- | --- | --- | --- |
| 1-1 | Items from empty tree | The tree is empty. | `t.items()` | `[]` |
| 2-1 | Items from single node | The tree has a single node with key `0` and value `a`. | `t.items()` | `[(0, "a")]` |
| 3-1 | Items from two nodes (ascending order) | The tree has two nodes with keys `-1` and `2`, linked so that `2` is the right child of `-1`. | `t.items()` | `[(-1, "a"), (2, "b")]` |
| 3-2 | Items from two nodes (descending order) | The tree has two nodes with keys `2` and `-1`, linked so that `-1` is the left child of `2`. | `t.items()` | `[(-1, "b"), (2, "a")]` |
| 4-1 | Items from three nodes (ascending order) | The tree has three nodes with keys `-1`, `0`, and `3`, linked in a right-leaning chain. | `t.items()` | `[(-1, "a"), (0, "b"), (3, "c")]` |
| 4-2 | Items from three nodes (descending order) | The tree has three nodes with keys `3`, `0`, and `-1`, linked in a left-leaning chain. | `t.items()` | `[(-1, "c"), (0, "b"), (3, "a")]` |
| 4-3 | Items from three nodes (mixed order) | The tree has three nodes with keys `0` (root), `-5` (left), and `10` (right). | `t.items()` | `[(-5, "b"), (0, "a"), (10, "c")]` |
