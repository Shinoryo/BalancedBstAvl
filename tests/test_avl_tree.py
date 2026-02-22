from __future__ import annotations

import random

import pytest

from avltree import AVLTree


# Custom class for testing arbitrary object values
class Person:
    """Simple class for testing custom objects as values in AVL tree."""

    def __init__(self, name: str, age: int) -> None:
        """Initialize a Person with name and age.

        Args:
            name: The person's name.
            age: The person's age.
        """
        self.name = name
        self.age = age

    def __eq__(self, other: object) -> bool:
        """Check equality based on name and age."""
        if not isinstance(other, Person):
            return NotImplemented
        return self.name == other.name and self.age == other.age

    def __hash__(self) -> int:
        """Return hash based on name and age."""
        return hash((self.name, self.age))

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Person(name={self.name!r}, age={self.age})"


def _assert_avl_balance(
    node: AVLTree | None,
    min_key: int | None = None,
    max_key: int | None = None,
) -> int:
    """Assert AVL balance and BST ordering for a subtree.

    Args:
        node: The subtree root to validate.
        min_key: Lower bound (exclusive) for keys in this subtree.
        max_key: Upper bound (exclusive) for keys in this subtree.

    Returns:
        The computed height of the subtree.
    """
    if node is None or node._key is None:
        return 0
    if min_key is not None:
        assert node._key > min_key
    if max_key is not None:
        assert node._key < max_key
    left_h = _assert_avl_balance(node._l, min_key, node._key)
    right_h = _assert_avl_balance(node._r, node._key, max_key)
    assert abs(left_h - right_h) <= 1
    return max(left_h, right_h) + 1


def _assert_height_consistency(node: AVLTree | None) -> int:
    """Assert that all node heights are correctly computed and consistent.

    Used for trees created through set/delete operations.

    Args:
        node: The subtree root to validate.

    Returns:
        The computed height of the subtree.
    """
    if node is None or node._key is None:
        return 0
    left_h = _assert_height_consistency(node._l)
    right_h = _assert_height_consistency(node._r)
    computed_h = max(left_h, right_h) + 1
    assert node._h == computed_h, (
        f"Node {node._key}: stored height {node._h}, computed height {computed_h}"
    )
    return computed_h


def _assert_balanced(tree: AVLTree) -> None:
    """Assert that the tree satisfies AVL balance and BST ordering.

    Also verifies that all node heights are correctly computed.

    Args:
        tree: The tree root to validate.
    """
    _assert_avl_balance(tree)
    _assert_height_consistency(tree)


# ==================== 1. __init__ (Constructor) ====================


@pytest.mark.init
def test_init_empty() -> None:
    """Test AVLTree() creates empty tree with all attributes set to defaults."""
    t = AVLTree()
    assert t._key is None
    assert t._value is None
    assert t._h == 0
    assert t._l is None
    assert t._r is None


@pytest.mark.init
def test_init_with_key() -> None:
    """Test AVLTree(10) creates tree with key, height=1, value=None."""
    t = AVLTree(10)
    assert t._key == 10
    assert t._value is None
    assert t._h == 1
    assert t._l is None
    assert t._r is None


@pytest.mark.init
def test_init_with_key_and_value() -> None:
    """Test AVLTree(5, 'val') creates tree with key and value."""
    t = AVLTree(5, "val")
    assert t._key == 5
    assert t._value == "val"
    assert t._h == 1


# ==================== 2. set(x: int, value: Any) ====================


@pytest.mark.set
def test_set_to_empty_tree() -> None:
    """Test adding a node to an empty tree."""
    t = AVLTree()
    t = t.set(0, "a")
    _assert_balanced(t)
    assert t._key == 0
    assert t._value == "a"


@pytest.mark.set
def test_set_update_root() -> None:
    """Test updating the root node."""
    t = AVLTree()
    t = t.set(0, "old")
    t = t.set(0, "new")
    _assert_balanced(t)
    assert t._key == 0
    assert t._value == "new"


@pytest.mark.set
def test_set_insert_left() -> None:
    """Test inserting a node to the left of root."""
    t = AVLTree()
    t = t.set(10, "a")
    t = t.set(-5, "b")
    _assert_balanced(t)
    assert t._key == 10
    assert t._l._key == -5
    assert t._l._value == "b"


@pytest.mark.set
def test_set_update_left() -> None:
    """Test updating a node to the left of root."""
    t = AVLTree()
    t = t.set(10, "a")
    t = t.set(-5, "b")
    t = t.set(-5, "b_new")
    _assert_balanced(t)
    assert t._l._value == "b_new"


@pytest.mark.set
def test_set_left_left_no_rebalance() -> None:
    """Test inserting a node to the left-left without rebalancing."""
    t = AVLTree()
    t = t.set(50, "a")
    t = t.set(30, "b")
    t = t.set(70, "c")
    t = t.set(60, "d")
    t = t.set(-20, "f")
    _assert_balanced(t)
    assert t._key == 50
    assert t._l._key == 30
    assert t._l._l._key == -20
    assert t._l._l._value == "f"
    assert t._r._key == 70
    assert t._r._l._key == 60
    assert t._r._l._value == "d"


@pytest.mark.set
def test_set_left_left_with_rebalance() -> None:
    """Test inserting a node to the left-left with rebalancing."""
    t = AVLTree()
    t = t.set(10, "a")
    t = t.set(-5, "b")
    t = t.set(-15, "c")
    _assert_balanced(t)
    assert t._key == -5
    assert t._l._key == -15
    assert t._l._value == "c"
    assert t._r._key == 10
    assert t._r._value == "a"


@pytest.mark.set
def test_set_update_left_left() -> None:
    """Test updating a node to the left-left of root."""
    t = AVLTree()
    t = t.set(50, "a")
    t = t.set(30, "b")
    t = t.set(70, "c")
    t = t.set(60, "d")
    t = t.set(-20, "d")
    t = t.set(-20, "d_new")
    _assert_balanced(t)
    assert t._l._l._value == "d_new"


@pytest.mark.set
def test_set_left_right_no_rebalance() -> None:
    """Test inserting a node to the left-right without rebalancing."""
    t = AVLTree()
    t = t.set(20, "a")
    t = t.set(10, "b")
    t = t.set(30, "c")
    _assert_balanced(t)
    assert t._key == 20
    assert t._l._key == 10
    assert t._l._value == "b"
    assert t._r._key == 30
    assert t._r._value == "c"


@pytest.mark.set
def test_set_left_right_with_rebalance() -> None:
    """Test inserting a node to the left-right with rebalancing."""
    t = AVLTree()
    t = t.set(10, "a")
    t = t.set(-15, "b")
    t = t.set(-5, "c")
    _assert_balanced(t)
    assert t._key == -5
    assert t._l._key == -15
    assert t._l._value == "b"
    assert t._r._key == 10
    assert t._r._value == "a"


@pytest.mark.set
def test_set_update_left_right() -> None:
    """Test updating a node to the left-right of root."""
    t = AVLTree()
    t = t.set(20, "a")
    t = t.set(-10, "b")
    t = t.set(30, "c")
    t = t.set(30, "c_new")
    _assert_balanced(t)
    assert t._r._value == "c_new"


@pytest.mark.set
def test_set_insert_right() -> None:
    """Test inserting a node to the right of root."""
    t = AVLTree()
    t = t.set(10, "a")
    t = t.set(15, "b")
    _assert_balanced(t)
    assert t._key == 10
    assert t._r._key == 15
    assert t._r._value == "b"


@pytest.mark.set
def test_set_update_right() -> None:
    """Test updating a node to the right of root."""
    t = AVLTree()
    t = t.set(10, "a")
    t = t.set(15, "b")
    t = t.set(15, "b_new")
    _assert_balanced(t)
    assert t._r._value == "b_new"


@pytest.mark.set
def test_set_right_left_no_rebalance() -> None:
    """Test inserting a node to the right-left without rebalancing."""
    t = AVLTree()
    t = t.set(20, "a")
    t = t.set(10, "b")
    t = t.set(40, "c")
    t = t.set(35, "d")
    _assert_balanced(t)
    assert t._key == 20
    assert t._l._key == 10
    assert t._l._value == "b"
    assert t._r._key == 40
    assert t._r._value == "c"
    assert t._r._l._key == 35
    assert t._r._l._value == "d"


@pytest.mark.set
def test_set_right_left_with_rebalance() -> None:
    """Test inserting a node to the right-left with rebalancing."""
    t = AVLTree()
    t = t.set(30, "a")
    t = t.set(40, "b")
    t = t.set(35, "c")
    _assert_balanced(t)
    assert t._key == 35
    assert t._l._key == 30
    assert t._l._value == "a"
    assert t._r._key == 40
    assert t._r._value == "b"


@pytest.mark.set
def test_set_update_right_left() -> None:
    """Test updating a node to the right-left of root."""
    t = AVLTree()
    t = t.set(20, "a")
    t = t.set(10, "b")
    t = t.set(40, "c")
    t = t.set(35, "d")
    t = t.set(35, "d_new")
    _assert_balanced(t)
    assert t._r._l._value == "d_new"


@pytest.mark.set
def test_set_right_right_no_rebalance() -> None:
    """Test inserting a node to the right-right without rebalancing."""
    t = AVLTree()
    t = t.set(20, "a")
    t = t.set(10, "b")
    t = t.set(25, "c")
    t = t.set(30, "d")
    _assert_balanced(t)
    assert t._key == 20
    assert t._l._key == 10
    assert t._l._value == "b"
    assert t._r._key == 25
    assert t._r._value == "c"
    assert t._r._r._key == 30
    assert t._r._r._value == "d"


@pytest.mark.set
def test_set_right_right_with_rebalance() -> None:
    """Test inserting a node to the right-right with rebalancing."""
    t = AVLTree()
    t = t.set(-30, "a")
    t = t.set(0, "b")
    t = t.set(30, "c")
    _assert_balanced(t)
    assert t._key == 0
    assert t._l._key == -30
    assert t._l._value == "a"
    assert t._r._key == 30
    assert t._r._value == "c"


@pytest.mark.set
def test_set_update_right_right() -> None:
    """Test updating a node to the right-right of root."""
    t = AVLTree()
    t = t.set(20, "a")
    t = t.set(-10, "b")
    t = t.set(25, "c")
    t = t.set(30, "d")
    t = t.set(30, "d_new")
    _assert_balanced(t)
    assert t._r._r._value == "d_new"


# ==================== 3. get(x: int, default=None) ====================


@pytest.mark.get
def test_get_from_root_found() -> None:
    """Test getting value from root when key is found."""
    t = AVLTree(0, "a")
    assert t.get(0) == "a"


@pytest.mark.get
def test_get_from_root_not_found() -> None:
    """Test getting value from root when key is not found."""
    t = AVLTree()
    assert t.get(5) is None


@pytest.mark.get
def test_get_from_left_found() -> None:
    """Test getting value from left when key is found."""
    t = AVLTree()
    t = t.set(10, "a")
    t = t.set(-5, "b")
    assert t.get(-5) == "b"


@pytest.mark.get
def test_get_from_left_not_found() -> None:
    """Test getting value from left when key is not found."""
    t = AVLTree()
    t = t.set(10, "a")
    t = t.set(-5, "b")
    assert t.get(-15) is None


@pytest.mark.get
def test_get_from_left_left_found() -> None:
    """Test getting value from left-left when key is found."""
    t = AVLTree()
    t = t.set(40, "a")
    t = t.set(20, "b")
    t = t.set(60, "c")
    t = t.set(-10, "d")
    assert t.get(-10) == "d"


@pytest.mark.get
def test_get_from_left_left_not_found() -> None:
    """Test getting value from left-left when key is not found."""
    t = AVLTree()
    t = t.set(40, "a")
    t = t.set(20, "b")
    t = t.set(60, "c")
    t = t.set(-10, "d")
    assert t.get(-25) is None


@pytest.mark.get
def test_get_from_left_right_found() -> None:
    """Test getting value from left-right when key is found."""
    t = AVLTree()
    t = t.set(40, "a")
    t = t.set(20, "b")
    t = t.set(60, "c")
    t = t.set(-10, "d")
    t = t.set(30, "e")
    assert t.get(30) == "e"


@pytest.mark.get
def test_get_from_left_right_not_found() -> None:
    """Test getting value from left-right when key is not found."""
    t = AVLTree()
    t = t.set(40, "a")
    t = t.set(20, "b")
    t = t.set(60, "c")
    t = t.set(10, "d")
    t = t.set(30, "e")
    assert t.get(15) is None


@pytest.mark.get
def test_get_from_right_found() -> None:
    """Test getting value from right when key is found."""
    t = AVLTree()
    t = t.set(0, "a")
    t = t.set(15, "b")
    assert t.get(15) == "b"


@pytest.mark.get
def test_get_from_right_not_found() -> None:
    """Test getting value from right when key is not found."""
    t = AVLTree()
    t = t.set(0, "a")
    t = t.set(15, "b")
    assert t.get(20) is None


@pytest.mark.get
def test_get_from_right_left_found() -> None:
    """Test getting value from right-left when key is found."""
    t = AVLTree()
    t = t.set(20, "a")
    t = t.set(10, "c")
    t = t.set(40, "b")
    t = t.set(30, "d")
    t = t.set(50, "e")
    assert t.get(30) == "d"


@pytest.mark.get
def test_get_from_right_left_not_found() -> None:
    """Test getting value from right-left when key is not found."""
    t = AVLTree()
    t = t.set(20, "a")
    t = t.set(10, "c")
    t = t.set(40, "b")
    t = t.set(30, "d")
    t = t.set(50, "e")
    assert t.get(25) is None


@pytest.mark.get
def test_get_from_right_right_found() -> None:
    """Test getting value from right-right when key is found."""
    t = AVLTree()
    t = t.set(20, "a")
    t = t.set(10, "b")
    t = t.set(30, "c")
    t = t.set(40, "d")
    assert t.get(40) == "d"


@pytest.mark.get
def test_get_from_right_right_not_found() -> None:
    """Test getting value from right-right when key is not found."""
    t = AVLTree()
    t = t.set(20, "a")
    t = t.set(10, "b")
    t = t.set(30, "c")
    t = t.set(40, "d")
    assert t.get(35) is None


@pytest.mark.get
def test_get_default_not_specified() -> None:
    """Test get with default value not specified."""
    t = AVLTree()
    assert t.get(5) is None


@pytest.mark.get
def test_get_default_specified() -> None:
    """Test get with default value specified."""
    t = AVLTree()
    assert t.get(5, "default") == "default"


# ==================== 4. find(x: int) ====================


@pytest.mark.find
def test_find_root_found() -> None:
    """Test finding root when key is found."""
    t = AVLTree(0, "a")
    assert t.find(0) is True


@pytest.mark.find
def test_find_root_not_found() -> None:
    """Test finding root when key is not found."""
    t = AVLTree()
    assert t.find(5) is False


@pytest.mark.find
def test_find_left_found() -> None:
    """Test finding left node when key is found."""
    t = AVLTree()
    t = t.set(10, "a")
    t = t.set(-5, "b")
    assert t.find(-5) is True


@pytest.mark.find
def test_find_left_not_found() -> None:
    """Test finding left node when key is not found."""
    t = AVLTree()
    t = t.set(10, "a")
    t = t.set(-5, "b")
    assert t.find(-15) is False


@pytest.mark.find
def test_find_left_left_found() -> None:
    """Test finding left-left node when key is found."""
    t = AVLTree()
    t = t.set(40, "a")
    t = t.set(20, "b")
    t = t.set(60, "c")
    t = t.set(-10, "d")
    assert t.find(-10) is True


@pytest.mark.find
def test_find_left_left_not_found() -> None:
    """Test finding left-left node when key is not found."""
    t = AVLTree()
    t = t.set(40, "a")
    t = t.set(20, "b")
    t = t.set(60, "c")
    t = t.set(-10, "d")
    assert t.find(-25) is False


@pytest.mark.find
def test_find_left_right_found() -> None:
    """Test finding left-right node when key is found."""
    t = AVLTree()
    t = t.set(40, "a")
    t = t.set(20, "b")
    t = t.set(60, "c")
    t = t.set(10, "d")
    t = t.set(30, "e")
    assert t.find(30) is True


@pytest.mark.find
def test_find_left_right_not_found() -> None:
    """Test finding left-right node when key is not found."""
    t = AVLTree()
    t = t.set(40, "a")
    t = t.set(20, "b")
    t = t.set(60, "c")
    t = t.set(10, "d")
    t = t.set(30, "e")
    assert t.find(15) is False


@pytest.mark.find
def test_find_right_found() -> None:
    """Test finding right node when key is found."""
    t = AVLTree()
    t = t.set(0, "a")
    t = t.set(15, "b")
    assert t.find(15) is True


@pytest.mark.find
def test_find_right_not_found() -> None:
    """Test finding right node when key is not found."""
    t = AVLTree()
    t = t.set(0, "a")
    t = t.set(15, "b")
    assert t.find(20) is False


@pytest.mark.find
def test_find_right_left_found() -> None:
    """Test finding right-left node when key is found."""
    t = AVLTree()
    t = t.set(20, "a")
    t = t.set(10, "c")
    t = t.set(40, "b")
    t = t.set(30, "d")
    t = t.set(50, "e")
    assert t.find(30) is True


@pytest.mark.find
def test_find_right_left_not_found() -> None:
    """Test finding right-left node when key is not found."""
    t = AVLTree()
    t = t.set(20, "a")
    t = t.set(10, "c")
    t = t.set(40, "b")
    t = t.set(30, "d")
    t = t.set(50, "e")
    assert t.find(25) is False


@pytest.mark.find
def test_find_right_right_found() -> None:
    """Test finding right-right node when key is found."""
    t = AVLTree()
    t = t.set(20, "a")
    t = t.set(10, "b")
    t = t.set(30, "c")
    t = t.set(40, "d")
    assert t.find(40) is True


@pytest.mark.find
def test_find_right_right_not_found() -> None:
    """Test finding right-right node when key is not found."""
    t = AVLTree()
    t = t.set(20, "a")
    t = t.set(10, "b")
    t = t.set(30, "c")
    t = t.set(40, "d")
    assert t.find(35) is False


# ==================== 5. delete(x: int) ====================


@pytest.mark.delete
def test_delete_root_no_rebalance() -> None:
    """Test deleting root without rebalancing needed."""
    t = AVLTree()
    t = t.set(10, "a")
    t = t.set(-5, "b")
    t = t.delete(10)
    _assert_balanced(t)
    assert t._key == -5
    assert t._value == "b"
    assert t._l is None
    assert t._r is None


@pytest.mark.delete
def test_delete_root_with_rebalance() -> None:
    """Test deleting root with rebalancing needed."""
    t = AVLTree()
    t = t.set(20, "b")
    t = t.set(10, "d")
    t = t.set(40, "a")
    t = t.set(5, "e")
    t = t.set(60, "c")
    t = t.delete(60)
    _assert_balanced(t)
    assert t._key == 20
    assert t._l._key == 10
    assert t._l._l._key == 5
    assert t._r._key == 40
    assert t._r._r is None or t._r._r._key is None


@pytest.mark.delete
def test_delete_root_not_found() -> None:
    """Test deleting from root when target not found."""
    t = AVLTree()
    t = t.delete(5)
    _assert_balanced(t)
    assert t._key is None
    assert t._l is None
    assert t._r is None


@pytest.mark.delete
def test_delete_root_leaf() -> None:
    """Test deleting root when it's a leaf."""
    t = AVLTree(5, "a")
    t = t.delete(5)
    _assert_balanced(t)
    assert t._key is None
    assert t._value is None
    assert t._l is None
    assert t._r is None


@pytest.mark.delete
def test_delete_left_no_rebalance() -> None:
    """Test deleting from left without rebalancing needed."""
    t = AVLTree()
    t = t.set(30, "a")
    t = t.set(-10, "b")
    t = t.set(40, "c")
    t = t.delete(-10)
    _assert_balanced(t)
    assert t._key == 30
    assert t._l is None or t._l._key is None
    assert t._r._key == 40


@pytest.mark.delete
def test_delete_left_with_rebalance() -> None:
    """Test deleting from left with rebalancing needed."""
    t = AVLTree()
    t = t.set(30, "b")
    t = t.set(20, "d")
    t = t.set(50, "a")
    t = t.set(10, "e")
    t = t.set(70, "c")
    t = t.delete(70)
    _assert_balanced(t)
    assert t._key == 30
    assert t._l._key == 20
    assert t._l._l._key == 10
    assert t._r._key == 50
    assert t._r._r is None or t._r._r._key is None


@pytest.mark.delete
def test_delete_left_not_found() -> None:
    """Test deleting from left when target not found."""
    t = AVLTree()
    t = t.set(30, "a")
    t = t.set(-10, "b")
    t = t.delete(-5)
    _assert_balanced(t)
    assert t._key == 30
    assert t._l._key == -10
    assert t._r is None


@pytest.mark.delete
def test_delete_left_with_children() -> None:
    """Test deleting node with two children from left subtree."""
    t = AVLTree()
    t = t.set(50, "a")
    t = t.set(30, "b")
    t = t.set(-20, "c")
    t = t.set(40, "d")
    t = t.delete(30)
    _assert_balanced(t)
    assert t._key in (40, 50)
    if t._key == 50:
        assert t._l._key == 40
        assert t._l._l._key == -20
        assert t._l._r is None or t._l._r._key is None
    else:
        assert t._l._key == -20
        assert t._r._key == 50


@pytest.mark.delete
def test_delete_left_left_no_rebalance() -> None:
    """Test deleting from left-left without rebalancing needed."""
    t = AVLTree()
    t = t.set(40, "a")
    t = t.set(20, "b")
    t = t.set(60, "c")
    t = t.set(10, "d")
    t = t.delete(10)
    _assert_balanced(t)
    assert t._key == 40
    assert t._l._key == 20
    assert t._l._l is None or t._l._l._key is None
    assert t._r._key == 60


@pytest.mark.delete
def test_delete_left_left_with_rebalance() -> None:
    """Test deleting from left-left with rebalancing needed."""
    t = AVLTree()
    t = t.set(40, "b")
    t = t.set(30, "d")
    t = t.set(60, "a")
    t = t.set(20, "e")
    t = t.set(80, "c")
    t = t.delete(80)
    _assert_balanced(t)
    assert t._key == 40
    assert t._l._key == 30
    assert t._l._l._key == 20
    assert t._r._key == 60
    assert t._r._r is None or t._r._r._key is None


@pytest.mark.delete
def test_delete_left_left_not_found() -> None:
    """Test deleting from left-left when target not found."""
    t = AVLTree()
    t = t.set(40, "a")
    t = t.set(20, "b")
    t = t.delete(5)
    _assert_balanced(t)
    assert t._key == 40
    assert t._l._key == 20
    assert t._r is None


@pytest.mark.delete
def test_delete_left_right_no_rebalance() -> None:
    """Test deleting from left-right without rebalancing needed."""
    t = AVLTree()
    t = t.set(40, "a")
    t = t.set(20, "b")
    t = t.set(60, "c")
    t = t.set(10, "d")
    t = t.set(30, "e")
    t = t.delete(30)
    _assert_balanced(t)
    assert t._key == 40
    assert t._l._key == 20
    assert t._l._l._key == 10
    assert t._l._r is None or t._l._r._key is None


@pytest.mark.delete
def test_delete_left_right_with_rebalance() -> None:
    """Test deleting from left-right with rebalancing needed."""
    t = AVLTree()
    t = t.set(30, "b")
    t = t.set(20, "d")
    t = t.set(50, "a")
    t = t.set(10, "e")
    t = t.set(25, "f")
    t = t.set(70, "c")
    t = t.delete(70)
    _assert_balanced(t)
    assert t._key == 30
    assert t._l._key == 20
    assert t._l._l._key == 10
    assert t._l._r._key == 25
    assert t._r._key == 50
    assert t._r._r is None or t._r._r._key is None


@pytest.mark.delete
def test_delete_left_right_not_found() -> None:
    """Test deleting from left-right when target not found."""
    t = AVLTree()
    t = t.set(40, "a")
    t = t.set(20, "b")
    t = t.set(60, "c")
    t = t.delete(15)
    _assert_balanced(t)
    assert t._key == 40
    assert t._l._key == 20
    assert t._r._key == 60


@pytest.mark.delete
def test_delete_right_no_rebalance() -> None:
    """Test deleting from right without rebalancing needed."""
    t = AVLTree()
    t = t.set(0, "a")
    t = t.set(15, "b")
    t = t.delete(15)
    _assert_balanced(t)
    assert t._key == 0
    assert t._l is None
    assert t._r is None or t._r._key is None


@pytest.mark.delete
def test_delete_right_with_rebalance() -> None:
    """Test deleting from right with rebalancing needed."""
    t = AVLTree()
    t = t.set(30, "c")
    t = t.set(20, "a")
    t = t.set(40, "d")
    t = t.set(10, "b")
    t = t.set(50, "e")
    t = t.delete(10)
    _assert_balanced(t)
    assert t._key == 30
    assert t._l._key == 20
    assert t._l._l is None or t._l._l._key is None
    assert t._r._key == 40
    assert t._r._r._key == 50


@pytest.mark.delete
def test_delete_right_not_found() -> None:
    """Test deleting from right when target not found."""
    t = AVLTree()
    t = t.set(10, "a")
    t = t.set(15, "b")
    t = t.delete(20)
    _assert_balanced(t)
    assert t._key == 10
    assert t._r._key == 15


@pytest.mark.delete
def test_delete_right_with_children() -> None:
    """Test deleting node with two children from right subtree."""
    t = AVLTree()
    t = t.set(40, "a")
    t = t.set(20, "b")
    t = t.set(60, "c")
    t = t.set(50, "d")
    t = t.delete(50)
    _assert_balanced(t)
    assert t._key == 40
    assert t._r._key == 60
    assert t._r._l is None or t._r._l._key is None


@pytest.mark.delete
def test_delete_right_left_no_rebalance() -> None:
    """Test deleting from right-left without rebalancing needed."""
    t = AVLTree()
    t = t.set(20, "a")
    t = t.set(10, "c")
    t = t.set(40, "b")
    t = t.set(30, "d")
    t = t.set(50, "e")
    t = t.delete(30)
    _assert_balanced(t)
    assert t._key == 20
    assert t._r._key == 40
    assert t._r._l is None or t._r._l._key is None
    assert t._r._r._key == 50


@pytest.mark.delete
def test_delete_right_left_with_rebalance() -> None:
    """Test deleting from right-left with rebalancing needed."""
    t = AVLTree()
    t = t.set(15, "e")
    t = t.set(10, "b")
    t = t.set(30, "a")
    t = t.set(5, "d")
    t = t.set(12, "f")
    t = t.set(50, "c")
    t = t.delete(5)
    _assert_balanced(t)
    assert t._key == 15
    assert t._l._key == 10
    assert t._l._l is None or t._l._l._key is None
    assert t._l._r._key == 12
    assert t._r._key == 30
    assert t._r._r._key == 50


@pytest.mark.delete
def test_delete_right_left_not_found() -> None:
    """Test deleting from right-left when target not found."""
    t = AVLTree()
    t = t.set(20, "a")
    t = t.set(10, "c")
    t = t.set(40, "b")
    t = t.delete(25)
    _assert_balanced(t)
    assert t._key == 20
    assert t._l._key == 10
    assert t._r._key == 40


@pytest.mark.delete
def test_delete_right_right_no_rebalance() -> None:
    """Test deleting from right-right without rebalancing needed."""
    t = AVLTree()
    t = t.set(20, "a")
    t = t.set(10, "b")
    t = t.set(30, "c")
    t = t.set(40, "d")
    t = t.delete(40)
    _assert_balanced(t)
    assert t._key == 20
    assert t._r._key == 30
    assert t._r._r is None or t._r._r._key is None


@pytest.mark.delete
def test_delete_right_right_with_rebalance() -> None:
    """Test deleting from right-right with rebalancing needed."""
    t = AVLTree()
    t = t.set(30, "c")
    t = t.set(20, "b")
    t = t.set(40, "d")
    t = t.set(10, "a")
    t = t.set(50, "e")
    t = t.delete(20)
    _assert_balanced(t)
    assert t._key == 30
    assert t._l._key == 10
    assert t._l._l is None
    assert t._r._key == 40
    assert t._r._r._key == 50


@pytest.mark.delete
def test_delete_right_right_not_found() -> None:
    """Test deleting from right-right when target not found."""
    t = AVLTree()
    t = t.set(20, "a")
    t = t.set(10, "b")
    t = t.set(30, "c")
    t = t.delete(35)
    _assert_balanced(t)
    assert t._key == 20
    assert t._l._key == 10
    assert t._r._key == 30


@pytest.mark.delete
def test_delete_2child_successor_is_leaf() -> None:
    """Test deleting 2-child node where successor is leaf."""
    t = AVLTree()
    t = t.set(30, "a")
    t = t.set(10, "b")
    t = t.set(50, "c")
    t = t.set(5, "d")
    t = t.set(20, "e")
    t = t.set(40, "f")
    t = t.set(60, "g")
    t = t.delete(30)
    _assert_balanced(t)
    assert t._key == 40
    assert t._value == "f"
    assert t._l._key == 10
    assert t._l._l._key == 5
    assert t._l._r._key == 20
    assert t._r._key == 50
    assert t._r._r._key == 60


@pytest.mark.delete
def test_delete_2child_successor_has_right_child() -> None:
    """Test deleting 2-child node where successor has right child."""
    t = AVLTree()
    t = t.set(30, "a")
    t = t.set(20, "b")
    t = t.set(40, "c")
    t = t.set(35, "d")
    t = t.set(50, "f")
    t = t.set(37, "e")
    t = t.delete(30)
    _assert_balanced(t)
    assert t._key == 35
    assert t._value == "d"
    assert t._l._key == 20
    assert t._r._key == 40
    assert t._r._l._key == 37
    assert t._r._r._key == 50


@pytest.mark.delete
def test_delete_2child_with_rebalance() -> None:
    """Test deleting 2-child node with rebalancing after replacement."""
    t = AVLTree()
    t = t.set(30, "b")
    t = t.set(20, "d")
    t = t.set(50, "a")
    t = t.set(10, "h")
    t = t.set(25, "j")
    t = t.set(40, "e")
    t = t.set(70, "c")
    t = t.set(5, "i")
    t = t.set(35, "k")
    t = t.set(45, "l")
    t = t.set(60, "f")
    t = t.set(80, "g")
    t = t.delete(30)
    _assert_balanced(t)
    assert t._key == 35
    assert t._value == "k"
    assert t._l._key == 20
    assert t._l._l._key == 10
    assert t._l._l._l._key == 5
    assert t._l._r._key == 25
    assert t._r._key == 50
    assert t._r._l._key == 40
    assert t._r._l._r._key == 45
    assert t._r._r._key == 70
    assert t._r._r._l._key == 60
    assert t._r._r._r._key == 80


# ==================== 6. items() ====================


@pytest.mark.items
def test_items_empty_tree() -> None:
    """Test items() on empty tree."""
    t = AVLTree()
    assert t.items() == []


@pytest.mark.items
def test_items_single_node() -> None:
    """Test items() with single node."""
    t = AVLTree(0, "a")
    assert t.items() == [(0, "a")]


@pytest.mark.items
def test_items_two_nodes_ascending() -> None:
    """Test items() with two nodes inserted in ascending order."""
    t = AVLTree()
    t = t.set(-1, "a")
    t = t.set(2, "b")
    assert t.items() == [(-1, "a"), (2, "b")]


@pytest.mark.items
def test_items_two_nodes_descending() -> None:
    """Test items() with two nodes inserted in descending order."""
    t = AVLTree()
    t = t.set(2, "a")
    t = t.set(-1, "b")
    assert t.items() == [(-1, "b"), (2, "a")]


@pytest.mark.items
def test_items_three_nodes_ascending() -> None:
    """Test items() with three nodes inserted in ascending order."""
    t = AVLTree()
    t = t.set(-1, "a")
    t = t.set(0, "b")
    t = t.set(3, "c")
    assert t.items() == [(-1, "a"), (0, "b"), (3, "c")]


@pytest.mark.items
def test_items_three_nodes_descending() -> None:
    """Test items() with three nodes inserted in descending order."""
    t = AVLTree()
    t = t.set(3, "a")
    t = t.set(0, "b")
    t = t.set(-1, "c")
    assert t.items() == [(-1, "c"), (0, "b"), (3, "a")]


@pytest.mark.items
def test_items_three_nodes_mixed() -> None:
    """Test items() with three nodes inserted in mixed order."""
    t = AVLTree()
    t = t.set(0, "a")
    t = t.set(-5, "b")
    t = t.set(10, "c")
    assert t.items() == [(-5, "b"), (0, "a"), (10, "c")]


# ==================== 7. Multiple Value Types (Integration Tests) ====================


@pytest.mark.valuetype
def test_value_with_bool() -> None:
    """Test storing boolean values."""
    t = AVLTree()
    t = t.set(1, value=True)
    t = t.set(-5, value=False)
    t = t.set(10, value=True)

    _assert_balanced(t)
    assert t.get(1) is True
    assert t.get(-5) is False
    assert t.get(10) is True


@pytest.mark.valuetype
def test_value_with_int() -> None:
    """Test storing integer values as values in AVL tree."""
    t = AVLTree()
    t = t.set(1, 42)
    t = t.set(-5, -100)
    t = t.set(10, 0)

    _assert_balanced(t)
    assert t.get(1) == 42
    assert t.get(-5) == -100
    assert t.get(10) == 0
    assert t.find(1) is True


@pytest.mark.valuetype
def test_value_with_float() -> None:
    """Test storing float as value in AVL tree."""
    t = AVLTree()
    t = t.set(1, 3.14)
    t = t.set(-5, 2.71)
    t = t.set(10, 1.41)

    _assert_balanced(t)
    assert abs(t.get(1) - 3.14) < 1e-9
    assert abs(t.get(-5) - 2.71) < 1e-9
    assert abs(t.get(10) - 1.41) < 1e-9


@pytest.mark.valuetype
def test_value_with_complex() -> None:
    """Test storing complex numbers as values."""
    t = AVLTree()
    t = t.set(1, 3 + 4j)
    t = t.set(-5, 1 + 1j)
    t = t.set(10, 5 + 2j)

    _assert_balanced(t)
    assert t.get(1) == 3 + 4j
    assert t.get(-5) == 1 + 1j
    assert t.get(10) == 5 + 2j


@pytest.mark.valuetype
def test_value_with_list() -> None:
    """Test storing list as value in AVL tree."""
    t = AVLTree()
    t = t.set(1, [10, 20, 30])
    t = t.set(-5, [1, 2])
    t = t.set(15, [100])

    _assert_balanced(t)
    assert t.get(1) == [10, 20, 30]
    assert t.get(-5) == [1, 2]
    assert t.get(15) == [100]
    assert t.find(1) is True


@pytest.mark.valuetype
def test_value_with_dict() -> None:
    """Test storing dict as value in AVL tree."""
    t = AVLTree()
    dict_a = {"name": "Alice", "age": 30}
    dict_b = {"name": "Bob", "age": 25}
    dict_c = {"name": "Charlie", "age": 35}

    t = t.set(1, dict_a)
    t = t.set(-10, dict_b)
    t = t.set(20, dict_c)

    _assert_balanced(t)
    assert t.get(1) == dict_a
    assert t.get(-10) == dict_b
    assert t.get(20) == dict_c
    assert t.find(-10) is True


@pytest.mark.valuetype
def test_value_with_tuple() -> None:
    """Test storing tuple as value in AVL tree."""
    t = AVLTree()
    tuple_a = (1, "one", True)
    tuple_b = (2, "two", False)
    tuple_c = (3, "three", True)

    t = t.set(0, tuple_a)
    t = t.set(-20, tuple_b)
    t = t.set(50, tuple_c)

    _assert_balanced(t)
    assert t.get(0) == tuple_a
    assert t.get(-20) == tuple_b
    assert t.get(50) == tuple_c
    assert t.get(0)[1] == "one"


@pytest.mark.valuetype
def test_value_with_nested_structures() -> None:
    """Test storing nested data structures (dict containing lists) as values."""
    t = AVLTree()
    complex_a = {"scores": [90, 85, 95], "name": "Student A"}
    complex_b = {"scores": [75, 80, 78], "name": "Student B"}

    t = t.set(1, complex_a)
    t = t.set(-5, complex_b)

    _assert_balanced(t)
    assert t.get(1)["scores"] == [90, 85, 95]
    assert t.get(-5)["name"] == "Student B"
    assert len(t.get(1)["scores"]) == 3


@pytest.mark.valuetype
def test_value_with_custom_object() -> None:
    """Test storing custom class instances as values."""
    alice = Person("Alice", 30)
    bob = Person("Bob", 25)
    charlie = Person("Charlie", 35)

    t = AVLTree()
    t = t.set(101, alice)
    t = t.set(-50, bob)
    t = t.set(200, charlie)

    _assert_balanced(t)
    assert t.get(101) == alice
    assert t.get(-50) == bob
    assert t.get(200) == charlie
    assert t.get(101).name == "Alice"
    assert t.get(-50).age == 25


@pytest.mark.valuetype
def test_value_update_with_different_type() -> None:
    """Test updating a value with a different type."""
    t = AVLTree()
    t = t.set(10, "string_value")
    _assert_balanced(t)
    assert t.get(10) == "string_value"

    # Update with a list
    t = t.set(10, [1, 2, 3])
    _assert_balanced(t)
    assert t.get(10) == [1, 2, 3]

    # Update with a dict
    t = t.set(10, {"key": "value"})
    _assert_balanced(t)
    assert t.get(10) == {"key": "value"}


# ==================== 8. Integration Tests - 0/1/2 Switch Coverage ====================
# Tests node count state transitions: 0 nodes, 1 node, 2 nodes
# Operations: set(new_key), delete(existing_key)


@pytest.mark.integration
def test_switch_0_empty_tree() -> None:
    """0-switch coverage: Initial state with empty tree (0 nodes)."""
    t = AVLTree()
    _assert_balanced(t)
    assert t.find(1) is False
    assert t.find(-5) is False


@pytest.mark.integration
def test_switch_0_single_node() -> None:
    """0-switch coverage: Initial state with single node (1 node)."""
    t = AVLTree()
    t = t.set(5, "a")
    _assert_balanced(t)
    assert t.find(5) is True
    assert t.get(5) == "a"


@pytest.mark.integration
def test_switch_0_two_nodes() -> None:
    """0-switch coverage: Initial state with two nodes (2 nodes)."""
    t = AVLTree()
    t = t.set(5, "a")
    t = t.set(-5, "b")
    _assert_balanced(t)
    assert t.find(5) is True
    assert t.find(-5) is True
    assert len(t.items()) == 2


@pytest.mark.integration
def test_switch_1_empty_to_single_via_set() -> None:
    """1-switch coverage: 0 nodes → set(new_key) → 1 node."""
    t = AVLTree()
    # 0 nodes state
    _assert_balanced(t)
    # Apply operation: set new key
    t = t.set(5, "a")
    # Verify 1 node state
    _assert_balanced(t)
    assert t.find(5) is True
    assert len(t.items()) == 1


@pytest.mark.integration
def test_switch_1_single_to_empty_via_delete() -> None:
    """1-switch coverage: 1 node → delete(existing_key) → 0 nodes."""
    t = AVLTree()
    t = t.set(5, "a")
    # 1 node state
    _assert_balanced(t)
    assert t.find(5) is True
    # Apply operation: delete existing key
    t = t.delete(5)
    # Verify 0 node state
    _assert_balanced(t)
    assert t.find(5) is False
    assert len(t.items()) == 0


@pytest.mark.integration
def test_switch_1_single_to_two_via_set() -> None:
    """1-switch coverage: 1 node → set(new_key) → 2 nodes."""
    t = AVLTree()
    t = t.set(5, "a")
    # 1 node state
    _assert_balanced(t)
    # Apply operation: set new key
    t = t.set(-5, "b")
    # Verify 2 node state
    _assert_balanced(t)
    assert t.find(5) is True
    assert t.find(-5) is True
    assert len(t.items()) == 2


@pytest.mark.integration
def test_switch_1_two_to_one_via_delete() -> None:
    """1-switch coverage: 2 nodes → delete(existing_key) → 1 node."""
    t = AVLTree()
    t = t.set(5, "a")
    t = t.set(-5, "b")
    # 2 node state
    _assert_balanced(t)
    assert len(t.items()) == 2
    # Apply operation: delete one key
    t = t.delete(5)
    # Verify 1 node state
    _assert_balanced(t)
    assert t.find(5) is False
    assert t.find(-5) is True
    assert len(t.items()) == 1


@pytest.mark.integration
def test_switch_1_two_to_three_via_set() -> None:
    """1-switch coverage: 2 nodes → set(new_key) → 3 nodes."""
    t = AVLTree()
    t = t.set(5, "a")
    t = t.set(-5, "b")
    # 2 node state
    _assert_balanced(t)
    # Apply operation: set new key
    t = t.set(10, "c")
    # Verify 3 node state
    _assert_balanced(t)
    assert t.find(5) is True
    assert t.find(-5) is True
    assert t.find(10) is True
    assert len(t.items()) == 3


@pytest.mark.integration
def test_switch_2_empty_set_set() -> None:
    """2-switch coverage: 0 nodes → set → 1 node → set → 2 nodes."""
    t = AVLTree()
    # 0 nodes state
    _assert_balanced(t)

    # Operation 1: set new key
    t = t.set(5, "a")
    # 1 node state
    _assert_balanced(t)
    assert len(t.items()) == 1

    # Operation 2: set another new key
    t = t.set(-5, "b")
    # 2 nodes state
    _assert_balanced(t)
    assert len(t.items()) == 2
    assert t.find(5) is True
    assert t.find(-5) is True


@pytest.mark.integration
def test_switch_2_empty_set_delete() -> None:
    """2-switch coverage: 0 nodes → set → 1 node → delete → 0 nodes."""
    t = AVLTree()
    # 0 nodes state
    _assert_balanced(t)

    # Operation 1: set new key
    t = t.set(5, "a")
    # 1 node state
    _assert_balanced(t)
    assert t.find(5) is True

    # Operation 2: delete that key
    t = t.delete(5)
    # 0 nodes state
    _assert_balanced(t)
    assert len(t.items()) == 0
    assert t.find(5) is False


@pytest.mark.integration
def test_switch_2_single_set_set() -> None:
    """2-switch coverage: 1 node → set → 2 nodes → set → 3 nodes."""
    t = AVLTree()
    t = t.set(5, "a")
    # 1 node state
    _assert_balanced(t)

    # Operation 1: set new key
    t = t.set(-5, "b")
    # 2 nodes state
    _assert_balanced(t)
    assert len(t.items()) == 2

    # Operation 2: set another new key
    t = t.set(15, "c")
    # 3 nodes state
    _assert_balanced(t)
    assert len(t.items()) == 3
    assert t.find(5) is True
    assert t.find(-5) is True
    assert t.find(15) is True


@pytest.mark.integration
def test_switch_2_single_set_delete() -> None:
    """2-switch coverage: 1 node → set → 2 nodes → delete → 1 node."""
    t = AVLTree()
    t = t.set(5, "a")
    # 1 node state
    _assert_balanced(t)

    # Operation 1: set new key
    t = t.set(-5, "b")
    # 2 nodes state
    _assert_balanced(t)
    assert len(t.items()) == 2

    # Operation 2: delete one key
    t = t.delete(-5)
    # 1 node state
    _assert_balanced(t)
    assert len(t.items()) == 1
    assert t.find(5) is True
    assert t.find(-5) is False


@pytest.mark.integration
def test_switch_2_single_delete_set() -> None:
    """2-switch coverage: 1 node → delete → 0 nodes → set → 1 node."""
    t = AVLTree()
    t = t.set(5, "a")
    # 1 node state
    _assert_balanced(t)

    # Operation 1: delete that key
    t = t.delete(5)
    # 0 nodes state
    _assert_balanced(t)
    assert len(t.items()) == 0

    # Operation 2: set new key
    t = t.set(10, "b")
    # 1 node state
    _assert_balanced(t)
    assert len(t.items()) == 1
    assert t.find(10) is True


@pytest.mark.integration
def test_switch_2_two_set_delete() -> None:
    """2-switch coverage: 2 nodes → set → 3 nodes → delete → 2 nodes."""
    t = AVLTree()
    t = t.set(5, "a")
    t = t.set(-5, "b")
    # 2 nodes state
    _assert_balanced(t)

    # Operation 1: set new key
    t = t.set(15, "c")
    # 3 nodes state
    _assert_balanced(t)
    assert len(t.items()) == 3

    # Operation 2: delete one key
    t = t.delete(15)
    # 2 nodes state
    _assert_balanced(t)
    assert len(t.items()) == 2
    assert t.find(5) is True
    assert t.find(-5) is True
    assert t.find(15) is False


@pytest.mark.integration
def test_switch_2_two_delete_set() -> None:
    """2-switch coverage: 2 nodes → delete → 1 node → set → 2 nodes."""
    t = AVLTree()
    t = t.set(5, "a")
    t = t.set(-5, "b")
    # 2 nodes state
    _assert_balanced(t)

    # Operation 1: delete one key
    t = t.delete(-5)
    # 1 node state
    _assert_balanced(t)
    assert len(t.items()) == 1
    assert t.find(5) is True

    # Operation 2: set new key
    t = t.set(10, "c")
    # 2 nodes state
    _assert_balanced(t)
    assert len(t.items()) == 2
    assert t.find(5) is True
    assert t.find(10) is True


@pytest.mark.integration
def test_switch_2_two_delete_delete() -> None:
    """2-switch coverage: 2 nodes → delete → 1 node → delete → 0 nodes."""
    t = AVLTree()
    t = t.set(5, "a")
    t = t.set(-5, "b")
    # 2 nodes state
    _assert_balanced(t)
    assert len(t.items()) == 2

    # Operation 1: delete one key
    t = t.delete(5)
    # 1 node state
    _assert_balanced(t)
    assert len(t.items()) == 1
    assert t.find(-5) is True

    # Operation 2: delete the remaining key
    t = t.delete(-5)
    # 0 nodes state
    _assert_balanced(t)
    assert len(t.items()) == 0
    assert t.find(-5) is False


# ==================== 9. Large Scale Performance and Balance Tests ====================


@pytest.mark.performance
def test_large_tree_100_nodes() -> None:
    """Insert 100 nodes and verify balance and height consistency.

    Tests AVL tree scalability and balance maintenance with 100 nodes.
    Validates that the tree remains balanced even at this scale.
    """
    t = AVLTree()
    keys = list(range(-50, 50))  # 100 keys
    for key in keys:
        t = t.set(key, f"val_{key}")
    _assert_balanced(t)
    assert len(t.items()) == 100
    for key in keys:
        assert t.find(key) is True


@pytest.mark.performance
def test_large_tree_500_nodes() -> None:
    """Insert 500 nodes and verify balance and height consistency.

    Tests AVL tree scalability and balance maintenance with 500 nodes.
    Validates that the tree remains balanced at medium-scale.
    """
    t = AVLTree()
    keys = list(range(-250, 250))  # 500 keys
    for key in keys:
        t = t.set(key, f"val_{key}")
    _assert_balanced(t)
    assert len(t.items()) == 500
    # Spot check some keys
    for key in [-250, -1, 0, 1, 249]:
        assert t.find(key) is True


@pytest.mark.performance
def test_large_tree_1000_nodes() -> None:
    """Insert 1000 nodes and verify balance and height consistency.

    Tests AVL tree scalability and balance maintenance with 1000 nodes.
    Validates that the tree remains balanced at large-scale.
    """
    t = AVLTree()
    keys = list(range(-500, 500))  # 1000 keys
    for key in keys:
        t = t.set(key, f"val_{key}")
    _assert_balanced(t)
    assert len(t.items()) == 1000
    # Spot check some keys
    for key in [-500, -1, 0, 1, 499]:
        assert t.find(key) is True


@pytest.mark.performance
def test_large_tree_sequential_insertions() -> None:
    """Build large tree with sequential insertions (ascending order).

    Tests AVL tree's ability to handle pathological insertion pattern.
    Verifies that ascending order insertions do not degrade balance.
    """
    t = AVLTree()
    num_nodes = 200
    for i in range(num_nodes):
        t = t.set(i, f"val_{i}")
    _assert_balanced(t)
    assert len(t.items()) == num_nodes
    items = t.items()
    # Verify items are in ascending order by key
    for i, (key, value) in enumerate(items):
        assert key == i
        assert value == f"val_{i}"


@pytest.mark.performance
def test_large_tree_random_insertions() -> None:
    """Build large tree with random insertions.

    Tests AVL tree's performance with typical real-world insertion pattern.
    Verifies balance is maintained with random insertion order.
    """
    t = AVLTree()
    num_nodes = 200
    keys = list(range(num_nodes))
    random.shuffle(keys)
    for key in keys:
        t = t.set(key, f"val_{key}")
    _assert_balanced(t)
    assert len(t.items()) == num_nodes
    # Verify all keys can be found
    for key in range(num_nodes):
        assert t.find(key) is True


@pytest.mark.performance
def test_large_tree_find_in_large_set() -> None:
    """Verify find operation works correctly in large tree.

    Tests lookup performance and correctness with 400-node tree.
    Validates that searching remains effective at large scale.
    """
    t = AVLTree()
    keys = list(range(-200, 200))  # 400 keys
    for key in keys:
        t = t.set(key, f"val_{key}")
    _assert_balanced(t)
    # Test finding existing keys
    for key in keys:
        assert t.find(key) is True
    # Test finding non-existing keys
    for non_key in [-201, 200, 500, -500]:
        assert t.find(non_key) is False


@pytest.mark.performance
def test_large_tree_get_in_large_set() -> None:
    """Verify get operation works correctly in large tree.

    Tests value retrieval performance and correctness with 300-node tree.
    Validates that get operation remains reliable at large scale.
    """
    t = AVLTree()
    keys = list(range(-150, 150))  # 300 keys
    for key in keys:
        t = t.set(key, f"val_{key}")
    _assert_balanced(t)
    # Test getting existing keys
    for key in keys:
        assert t.get(key) == f"val_{key}"
    # Test getting non-existing keys with default
    assert t.get(-151, "default") == "default"
    assert t.get(150, "default") == "default"


@pytest.mark.performance
def test_large_tree_delete_multiple_from_large_set() -> None:
    """Delete multiple random keys from large tree and verify balance.

    Tests deletion performance and balance maintenance with 100-node tree.
    Validates that deleting 30% of nodes maintains AVL properties.
    """
    t = AVLTree()
    keys = list(range(100))
    for key in keys:
        t = t.set(key, f"val_{key}")
    _assert_balanced(t)
    assert len(t.items()) == 100
    # Delete 30 random keys
    keys_to_delete = random.sample(keys, 30)
    for key in keys_to_delete:
        t = t.delete(key)
        _assert_balanced(t)
    assert len(t.items()) == 70
    # Verify deleted keys are not found
    for key in keys_to_delete:
        assert t.find(key) is False
    # Verify remaining keys are found
    remaining_keys = [k for k in keys if k not in keys_to_delete]
    for key in remaining_keys:
        assert t.find(key) is True


@pytest.mark.performance
def test_large_tree_sequential_deletions() -> None:
    """Build large tree then delete all nodes sequentially, verifying balance.

    Tests complete deletion sequence with continuous balance verification.
    Validates that tree remains balanced through all intermediate states.
    """
    t = AVLTree()
    keys = list(range(50))
    for key in keys:
        t = t.set(key, f"val_{key}")
    _assert_balanced(t)
    assert len(t.items()) == 50
    # Delete all keys in reverse order
    for key in reversed(keys):
        t = t.delete(key)
        _assert_balanced(t)
    assert len(t.items()) == 0
    # Verify all keys are gone
    for key in keys:
        assert t.find(key) is False


@pytest.mark.performance
def test_large_tree_mixed_operations() -> None:
    """Perform mixed set/delete operations on large tree.

    Tests real-world scenario with insertion, deletion, and re-insertion.
    Validates balance maintenance through complex operation sequence.
    """
    t = AVLTree()
    # Initial insertions
    for i in range(100):
        t = t.set(i, f"val_{i}")
    _assert_balanced(t)
    # Delete every third key
    for i in range(0, 100, 3):
        t = t.delete(i)
    _assert_balanced(t)
    remaining_count = len(t.items())
    # Insert new keys in the gaps
    for i in range(100, 150):
        t = t.set(i, f"new_val_{i}")
    _assert_balanced(t)
    # Final verification
    assert len(t.items()) > remaining_count
    for i in range(100, 150):
        assert t.find(i) is True
