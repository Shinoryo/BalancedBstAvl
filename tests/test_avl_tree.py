from __future__ import annotations

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


def _rebuild_heights(node: AVLTree | None) -> None:
    """Rebuild all node heights in a manually constructed tree.

    Used to fix heights in trees constructed via direct assignment of children.
    Performs post-order traversal to correctly compute heights bottom-up.

    Args:
        node: The subtree root to rebuild.
    """
    if node is None or node._key is None:
        return
    _rebuild_heights(node._l)
    _rebuild_heights(node._r)
    # Recalculate height based on children
    left_h = node._l._h if (node._l and node._l._key is not None) else 0
    right_h = node._r._h if (node._r and node._r._key is not None) else 0
    node._h = max(left_h, right_h) + 1


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
    t = AVLTree(10, "a")
    t._l = AVLTree(-5, "b")
    assert t.get(-5) == "b"


@pytest.mark.get
def test_get_from_left_not_found() -> None:
    """Test getting value from left when key is not found."""
    t = AVLTree(10, "a")
    t._l = AVLTree(-5, "b")
    assert t.get(-15) is None


@pytest.mark.get
def test_get_from_left_left_found() -> None:
    """Test getting value from left-left when key is found."""
    t = AVLTree(40, "a")
    t._l = AVLTree(20, "b")
    t._r = AVLTree(60, "c")
    t._l._l = AVLTree(-10, "d")
    assert t.get(-10) == "d"


@pytest.mark.get
def test_get_from_left_left_not_found() -> None:
    """Test getting value from left-left when key is not found."""
    t = AVLTree(40, "a")
    t._l = AVLTree(20, "b")
    t._r = AVLTree(60, "c")
    t._l._l = AVLTree(-10, "d")
    assert t.get(-25) is None


@pytest.mark.get
def test_get_from_left_right_found() -> None:
    """Test getting value from left-right when key is found."""
    t = AVLTree(40, "a")
    t._l = AVLTree(20, "b")
    t._r = AVLTree(60, "c")
    t._l._l = AVLTree(-10, "d")
    t._l._r = AVLTree(30, "e")
    assert t.get(30) == "e"


@pytest.mark.get
def test_get_from_left_right_not_found() -> None:
    """Test getting value from left-right when key is not found."""
    t = AVLTree(40, "a")
    t._l = AVLTree(20, "b")
    t._r = AVLTree(60, "c")
    t._l._l = AVLTree(10, "d")
    t._l._r = AVLTree(30, "e")
    assert t.get(15) is None


@pytest.mark.get
def test_get_from_right_found() -> None:
    """Test getting value from right when key is found."""
    t = AVLTree(0, "a")
    t._r = AVLTree(15, "b")
    assert t.get(15) == "b"


@pytest.mark.get
def test_get_from_right_not_found() -> None:
    """Test getting value from right when key is not found."""
    t = AVLTree(0, "a")
    t._r = AVLTree(15, "b")
    assert t.get(20) is None


@pytest.mark.get
def test_get_from_right_left_found() -> None:
    """Test getting value from right-left when key is found."""
    t = AVLTree(20, "a")
    t._l = AVLTree(10, "c")
    t._r = AVLTree(40, "b")
    t._r._l = AVLTree(30, "d")
    t._r._r = AVLTree(50, "e")
    assert t.get(30) == "d"


@pytest.mark.get
def test_get_from_right_left_not_found() -> None:
    """Test getting value from right-left when key is not found."""
    t = AVLTree(20, "a")
    t._l = AVLTree(10, "c")
    t._r = AVLTree(40, "b")
    t._r._l = AVLTree(30, "d")
    t._r._r = AVLTree(50, "e")
    assert t.get(25) is None


@pytest.mark.get
def test_get_from_right_right_found() -> None:
    """Test getting value from right-right when key is found."""
    t = AVLTree(20, "a")
    t._l = AVLTree(10, "b")
    t._r = AVLTree(30, "c")
    t._r._r = AVLTree(40, "d")
    assert t.get(40) == "d"


@pytest.mark.get
def test_get_from_right_right_not_found() -> None:
    """Test getting value from right-right when key is not found."""
    t = AVLTree(20, "a")
    t._l = AVLTree(10, "b")
    t._r = AVLTree(30, "c")
    t._r._r = AVLTree(40, "d")
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
    t = AVLTree(10, "a")
    t._l = AVLTree(-5, "b")
    assert t.find(-5) is True


@pytest.mark.find
def test_find_left_not_found() -> None:
    """Test finding left node when key is not found."""
    t = AVLTree(10, "a")
    t._l = AVLTree(-5, "b")
    assert t.find(-15) is False


@pytest.mark.find
def test_find_left_left_found() -> None:
    """Test finding left-left node when key is found."""
    t = AVLTree(40, "a")
    t._l = AVLTree(20, "b")
    t._r = AVLTree(60, "c")
    t._l._l = AVLTree(-10, "d")
    assert t.find(-10) is True


@pytest.mark.find
def test_find_left_left_not_found() -> None:
    """Test finding left-left node when key is not found."""
    t = AVLTree(40, "a")
    t._l = AVLTree(20, "b")
    t._r = AVLTree(60, "c")
    t._l._l = AVLTree(-10, "d")
    assert t.find(-25) is False


@pytest.mark.find
def test_find_left_right_found() -> None:
    """Test finding left-right node when key is found."""
    t = AVLTree(40, "a")
    t._l = AVLTree(20, "b")
    t._r = AVLTree(60, "c")
    t._l._l = AVLTree(10, "d")
    t._l._r = AVLTree(30, "e")
    assert t.find(30) is True


@pytest.mark.find
def test_find_left_right_not_found() -> None:
    """Test finding left-right node when key is not found."""
    t = AVLTree(40, "a")
    t._l = AVLTree(20, "b")
    t._r = AVLTree(60, "c")
    t._l._l = AVLTree(10, "d")
    t._l._r = AVLTree(30, "e")
    assert t.find(15) is False


@pytest.mark.find
def test_find_right_found() -> None:
    """Test finding right node when key is found."""
    t = AVLTree(0, "a")
    t._r = AVLTree(15, "b")
    assert t.find(15) is True


@pytest.mark.find
def test_find_right_not_found() -> None:
    """Test finding right node when key is not found."""
    t = AVLTree(0, "a")
    t._r = AVLTree(15, "b")
    assert t.find(20) is False


@pytest.mark.find
def test_find_right_left_found() -> None:
    """Test finding right-left node when key is found."""
    t = AVLTree(20, "a")
    t._l = AVLTree(10, "c")
    t._r = AVLTree(40, "b")
    t._r._l = AVLTree(30, "d")
    t._r._r = AVLTree(50, "e")
    assert t.find(30) is True


@pytest.mark.find
def test_find_right_left_not_found() -> None:
    """Test finding right-left node when key is not found."""
    t = AVLTree(20, "a")
    t._l = AVLTree(10, "c")
    t._r = AVLTree(40, "b")
    t._r._l = AVLTree(30, "d")
    t._r._r = AVLTree(50, "e")
    assert t.find(25) is False


@pytest.mark.find
def test_find_right_right_found() -> None:
    """Test finding right-right node when key is found."""
    t = AVLTree(20, "a")
    t._l = AVLTree(10, "b")
    t._r = AVLTree(30, "c")
    t._r._r = AVLTree(40, "d")
    assert t.find(40) is True


@pytest.mark.find
def test_find_right_right_not_found() -> None:
    """Test finding right-right node when key is not found."""
    t = AVLTree(20, "a")
    t._l = AVLTree(10, "b")
    t._r = AVLTree(30, "c")
    t._r._r = AVLTree(40, "d")
    assert t.find(35) is False


# ==================== 5. delete(x: int) ====================


@pytest.mark.delete
def test_delete_root_no_rebalance() -> None:
    """Test deleting root without rebalancing needed."""
    left = AVLTree(-5, "b")
    t = AVLTree(10, "a")
    t._l = left
    t = t.delete(10)
    _assert_balanced(t)
    assert t._key == -5
    assert t._value == "b"
    assert t._l is None
    assert t._r is None


@pytest.mark.delete
def test_delete_root_with_rebalance() -> None:
    """Test deleting root with rebalancing needed."""
    left_left = AVLTree(5, "e")
    left = AVLTree(10, "d")
    left._l = left_left
    right_right = AVLTree(60, "c")
    right = AVLTree(40, "a")
    right._r = right_right
    t = AVLTree(20, "b")
    t._l = left
    t._r = right
    _rebuild_heights(t)
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
    left = AVLTree(-10, "b")
    right = AVLTree(40, "c")
    t = AVLTree(30, "a")
    t._l = left
    t._r = right
    t = t.delete(-10)
    _assert_balanced(t)
    assert t._key == 30
    assert t._l is None or t._l._key is None
    assert t._r._key == 40


@pytest.mark.delete
def test_delete_left_with_rebalance() -> None:
    """Test deleting from left with rebalancing needed."""
    left_left = AVLTree(10, "e")
    left = AVLTree(20, "d")
    left._l = left_left
    right_right = AVLTree(70, "c")
    right = AVLTree(50, "a")
    right._r = right_right
    t = AVLTree(30, "b")
    t._l = left
    t._r = right
    _rebuild_heights(t)
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
    left = AVLTree(-10, "b")
    t = AVLTree(30, "a")
    t._l = left
    t = t.delete(-5)
    _assert_balanced(t)
    assert t._key == 30
    assert t._l._key == -10
    assert t._r is None


@pytest.mark.delete
def test_delete_left_with_children() -> None:
    """Test deleting node with two children from left subtree."""
    left_left = AVLTree(-20, "c")
    left_right = AVLTree(40, "d")
    left = AVLTree(30, "b")
    left._l = left_left
    left._r = left_right
    t = AVLTree(50, "a")
    t._l = left
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
    left_left = AVLTree(10, "d")
    left = AVLTree(20, "b")
    left._l = left_left
    right = AVLTree(60, "c")
    t = AVLTree(40, "a")
    t._l = left
    t._r = right
    t = t.delete(10)
    _assert_balanced(t)
    assert t._key == 40
    assert t._l._key == 20
    assert t._l._l is None or t._l._l._key is None
    assert t._r._key == 60


@pytest.mark.delete
def test_delete_left_left_with_rebalance() -> None:
    """Test deleting from left-left with rebalancing needed."""
    left_left = AVLTree(20, "e")
    left = AVLTree(30, "d")
    left._l = left_left
    right_right = AVLTree(80, "c")
    right = AVLTree(60, "a")
    right._r = right_right
    t = AVLTree(40, "b")
    t._l = left
    t._r = right
    _rebuild_heights(t)
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
    left = AVLTree(20, "b")
    t = AVLTree(40, "a")
    t._l = left
    t = t.delete(5)
    _assert_balanced(t)
    assert t._key == 40
    assert t._l._key == 20
    assert t._r is None


@pytest.mark.delete
def test_delete_left_right_no_rebalance() -> None:
    """Test deleting from left-right without rebalancing needed."""
    left_left = AVLTree(10, "d")
    left_right = AVLTree(30, "e")
    left = AVLTree(20, "b")
    left._l = left_left
    left._r = left_right
    right = AVLTree(60, "c")
    t = AVLTree(40, "a")
    t._l = left
    t._r = right
    t = t.delete(30)
    _assert_balanced(t)
    assert t._key == 40
    assert t._l._key == 20
    assert t._l._l._key == 10
    assert t._l._r is None or t._l._r._key is None


@pytest.mark.delete
def test_delete_left_right_with_rebalance() -> None:
    """Test deleting from left-right with rebalancing needed."""
    left_left = AVLTree(10, "e")
    left_right = AVLTree(25, "f")
    left = AVLTree(20, "d")
    left._l = left_left
    left._r = left_right
    right_right = AVLTree(70, "c")
    right = AVLTree(50, "a")
    right._r = right_right
    t = AVLTree(30, "b")
    t._l = left
    t._r = right
    _rebuild_heights(t)
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
    left = AVLTree(20, "b")
    right = AVLTree(60, "c")
    t = AVLTree(40, "a")
    t._l = left
    t._r = right
    t = t.delete(15)
    _assert_balanced(t)
    assert t._key == 40
    assert t._l._key == 20
    assert t._r._key == 60


@pytest.mark.delete
def test_delete_right_no_rebalance() -> None:
    """Test deleting from right without rebalancing needed."""
    right = AVLTree(15, "b")
    t = AVLTree(0, "a")
    t._r = right
    t = t.delete(15)
    _assert_balanced(t)
    assert t._key == 0
    assert t._l is None
    assert t._r is None or t._r._key is None


@pytest.mark.delete
def test_delete_right_with_rebalance() -> None:
    """Test deleting from right with rebalancing needed."""
    left_left = AVLTree(10, "b")
    left = AVLTree(20, "a")
    left._l = left_left
    right_right = AVLTree(50, "e")
    right = AVLTree(40, "d")
    right._r = right_right
    t = AVLTree(30, "c")
    t._l = left
    t._r = right
    _rebuild_heights(t)
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
    right = AVLTree(15, "b")
    t = AVLTree(10, "a")
    t._r = right
    t = t.delete(20)
    _assert_balanced(t)
    assert t._key == 10
    assert t._r._key == 15


@pytest.mark.delete
def test_delete_right_with_children() -> None:
    """Test deleting node with two children from right subtree."""
    left = AVLTree(20, "b")
    right_left = AVLTree(50, "d")
    right = AVLTree(60, "c")
    right._l = right_left
    t = AVLTree(40, "a")
    t._l = left
    t._r = right
    t = t.delete(50)
    _assert_balanced(t)
    assert t._key == 40
    assert t._r._key == 60
    assert t._r._l is None or t._r._l._key is None


@pytest.mark.delete
def test_delete_right_left_no_rebalance() -> None:
    """Test deleting from right-left without rebalancing needed."""
    left = AVLTree(10, "c")
    right_left = AVLTree(30, "d")
    right_right = AVLTree(50, "e")
    right = AVLTree(40, "b")
    right._l = right_left
    right._r = right_right
    t = AVLTree(20, "a")
    t._l = left
    t._r = right
    t = t.delete(30)
    _assert_balanced(t)
    assert t._key == 20
    assert t._r._key == 40
    assert t._r._l is None or t._r._l._key is None
    assert t._r._r._key == 50


@pytest.mark.delete
def test_delete_right_left_with_rebalance() -> None:
    """Test deleting from right-left with rebalancing needed."""
    left_left = AVLTree(5, "d")
    left_right = AVLTree(12, "f")
    left = AVLTree(10, "b")
    left._l = left_left
    left._r = left_right
    right_right = AVLTree(50, "c")
    right = AVLTree(30, "a")
    right._r = right_right
    t = AVLTree(15, "e")
    t._l = left
    t._r = right
    _rebuild_heights(t)
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
    left = AVLTree(10, "c")
    right = AVLTree(40, "b")
    t = AVLTree(20, "a")
    t._l = left
    t._r = right
    t = t.delete(25)
    _assert_balanced(t)
    assert t._key == 20
    assert t._l._key == 10
    assert t._r._key == 40


@pytest.mark.delete
def test_delete_right_right_no_rebalance() -> None:
    """Test deleting from right-right without rebalancing needed."""
    left = AVLTree(10, "b")
    right_right = AVLTree(40, "d")
    right = AVLTree(30, "c")
    right._r = right_right
    t = AVLTree(20, "a")
    t._l = left
    t._r = right
    t = t.delete(40)
    _assert_balanced(t)
    assert t._key == 20
    assert t._r._key == 30
    assert t._r._r is None or t._r._r._key is None


@pytest.mark.delete
def test_delete_right_right_with_rebalance() -> None:
    """Test deleting from right-right with rebalancing needed."""
    left_left = AVLTree(10, "a")
    left = AVLTree(20, "b")
    left._l = left_left
    right_right = AVLTree(50, "e")
    right = AVLTree(40, "d")
    right._r = right_right
    t = AVLTree(30, "c")
    t._l = left
    t._r = right
    _rebuild_heights(t)
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
    left = AVLTree(10, "b")
    right = AVLTree(30, "c")
    t = AVLTree(20, "a")
    t._l = left
    t._r = right
    t = t.delete(35)
    _assert_balanced(t)
    assert t._key == 20
    assert t._l._key == 10
    assert t._r._key == 30


@pytest.mark.delete
def test_delete_2child_successor_is_leaf() -> None:
    """Test deleting 2-child node where successor is leaf."""
    left_left = AVLTree(5, "d")
    left_right = AVLTree(20, "e")
    left = AVLTree(10, "b")
    left._l = left_left
    left._r = left_right
    right_left = AVLTree(40, "f")
    right_right = AVLTree(60, "g")
    right = AVLTree(50, "c")
    right._l = right_left
    right._r = right_right
    t = AVLTree(30, "a")
    t._l = left
    t._r = right
    _rebuild_heights(t)
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
    left = AVLTree(20, "b")
    right_left_right = AVLTree(37, "e")
    right_left = AVLTree(35, "d")
    right_left._r = right_left_right
    right_right = AVLTree(50, "f")
    right = AVLTree(40, "c")
    right._l = right_left
    right._r = right_right
    t = AVLTree(30, "a")
    t._l = left
    t._r = right
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
    left_left_left = AVLTree(5, "i")
    left_left = AVLTree(10, "h")
    left_left._l = left_left_left
    left_left._h = 2
    left_right = AVLTree(25, "j")
    left = AVLTree(20, "d")
    left._l = left_left
    left._r = left_right
    left._h = 3
    right_left_left = AVLTree(35, "k")
    right_left_right = AVLTree(45, "l")
    right_left = AVLTree(40, "e")
    right_left._l = right_left_left
    right_left._r = right_left_right
    right_left._h = 2
    right_right_left = AVLTree(60, "f")
    right_right_right = AVLTree(80, "g")
    right_right = AVLTree(70, "c")
    right_right._l = right_right_left
    right_right._r = right_right_right
    right_right._h = 2
    right = AVLTree(50, "a")
    right._l = right_left
    right._r = right_right
    right._h = 3
    t = AVLTree(30, "b")
    t._l = left
    t._r = right
    t._h = 4
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
    right = AVLTree(2, "b")
    t = AVLTree(-1, "a")
    t._r = right
    assert t.items() == [(-1, "a"), (2, "b")]


@pytest.mark.items
def test_items_two_nodes_descending() -> None:
    """Test items() with two nodes inserted in descending order."""
    left = AVLTree(-1, "b")
    t = AVLTree(2, "a")
    t._l = left
    assert t.items() == [(-1, "b"), (2, "a")]


@pytest.mark.items
def test_items_three_nodes_ascending() -> None:
    """Test items() with three nodes inserted in ascending order."""
    right_right = AVLTree(3, "c")
    right = AVLTree(0, "b")
    right._r = right_right
    t = AVLTree(-1, "a")
    t._r = right
    assert t.items() == [(-1, "a"), (0, "b"), (3, "c")]


@pytest.mark.items
def test_items_three_nodes_descending() -> None:
    """Test items() with three nodes inserted in descending order."""
    left_left = AVLTree(-1, "c")
    left = AVLTree(0, "b")
    left._l = left_left
    t = AVLTree(3, "a")
    t._l = left
    assert t.items() == [(-1, "c"), (0, "b"), (3, "a")]


@pytest.mark.items
def test_items_three_nodes_mixed() -> None:
    """Test items() with three nodes inserted in mixed order."""
    left = AVLTree(-5, "b")
    right = AVLTree(10, "c")
    t = AVLTree(0, "a")
    t._l = left
    t._r = right
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
