import pytest

from avltree import AVLTree


def _assert_avl_balance(node: AVLTree | None, min_key: int | None = None, max_key: int | None = None) -> int:
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


def _assert_balanced(tree: AVLTree) -> None:
    _assert_avl_balance(tree)

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
    t = t.set(5, "a")
    _assert_balanced(t)
    assert t._key == 5
    assert t._value == "a"


@pytest.mark.set
def test_set_update_root() -> None:
    """Test updating the root node."""
    t = AVLTree()
    t = t.set(5, "old")
    t = t.set(5, "new")
    _assert_balanced(t)
    assert t._key == 5
    assert t._value == "new"


@pytest.mark.set
def test_set_insert_left() -> None:
    """Test inserting a node to the left of root."""
    t = AVLTree()
    t = t.set(10, "a")
    t = t.set(5, "b")
    _assert_balanced(t)
    assert t._key == 10
    assert t._l._key == 5
    assert t._l._value == "b"


@pytest.mark.set
def test_set_update_left() -> None:
    """Test updating a node to the left of root."""
    t = AVLTree()
    t = t.set(10, "a")
    t = t.set(5, "b")
    t = t.set(5, "b_new")
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
    t = t.set(20, "f")
    _assert_balanced(t)
    assert t._key == 50
    assert t._l._key == 30
    assert t._l._l._key == 20
    assert t._l._l._value == "f"
    assert t._r._key == 70
    assert t._r._l._key == 60
    assert t._r._l._value == "d"


@pytest.mark.set
def test_set_left_left_with_rebalance() -> None:
    """Test inserting a node to the left-left with rebalancing."""
    t = AVLTree()
    t = t.set(10, "a")
    t = t.set(5, "b")
    t = t.set(3, "c")
    _assert_balanced(t)
    assert t._key == 5
    assert t._l._key == 3
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
    t = t.set(20, "d")
    t = t.set(20, "d_new")
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
    t = t.set(3, "b")
    t = t.set(5, "c")
    _assert_balanced(t)
    assert t._key == 5
    assert t._l._key == 3
    assert t._l._value == "b"
    assert t._r._key == 10
    assert t._r._value == "a"


@pytest.mark.set
def test_set_update_left_right() -> None:
    """Test updating a node to the left-right of root."""
    t = AVLTree()
    t = t.set(20, "a")
    t = t.set(10, "b")
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
    t = t.set(30, "a")
    t = t.set(40, "b")
    t = t.set(50, "c")
    _assert_balanced(t)
    assert t._key == 40
    assert t._l._key == 30
    assert t._l._value == "a"
    assert t._r._key == 50
    assert t._r._value == "c"


@pytest.mark.set
def test_set_update_right_right() -> None:
    """Test updating a node to the right-right of root."""
    t = AVLTree()
    t = t.set(20, "a")
    t = t.set(10, "b")
    t = t.set(25, "c")
    t = t.set(30, "d")
    t = t.set(30, "d_new")
    _assert_balanced(t)
    assert t._r._r._value == "d_new"


# ==================== 3. get(x: int, default=None) ====================

@pytest.mark.get
def test_get_from_root_exists() -> None:
    """Test getting value from root that exists."""
    t = AVLTree(10, "a")
    assert t.get(10) == "a"


@pytest.mark.get
def test_get_from_root_not_exists() -> None:
    """Test getting value from root that doesn't exist."""
    t = AVLTree()
    assert t.get(5) is None


@pytest.mark.get
def test_get_from_left_exists() -> None:
    """Test getting value from left that exists."""
    t = AVLTree(10, "a")
    t._l = AVLTree(5, "b")
    assert t.get(5) == "b"


@pytest.mark.get
def test_get_from_left_not_exists() -> None:
    """Test getting value from left that doesn't exist."""
    t = AVLTree(10, "a")
    t._l = AVLTree(5, "b")
    assert t.get(3) is None


@pytest.mark.get
def test_get_from_left_left_exists() -> None:
    """Test getting value from left-left that exists."""
    t = AVLTree(40, "a")
    t._l = AVLTree(20, "b")
    t._r = AVLTree(60, "c")
    t._l._l = AVLTree(10, "d")
    assert t.get(10) == "d"


@pytest.mark.get
def test_get_from_left_left_not_exists() -> None:
    """Test getting value from left-left that doesn't exist."""
    t = AVLTree(40, "a")
    t._l = AVLTree(20, "b")
    t._r = AVLTree(60, "c")
    t._l._l = AVLTree(10, "d")
    assert t.get(5) is None


@pytest.mark.get
def test_get_from_left_right_exists() -> None:
    """Test getting value from left-right that exists."""
    t = AVLTree(40, "a")
    t._l = AVLTree(20, "b")
    t._r = AVLTree(60, "c")
    t._l._l = AVLTree(10, "d")
    t._l._r = AVLTree(30, "e")
    assert t.get(30) == "e"


@pytest.mark.get
def test_get_from_left_right_not_exists() -> None:
    """Test getting value from left-right that doesn't exist."""
    t = AVLTree(40, "a")
    t._l = AVLTree(20, "b")
    t._r = AVLTree(60, "c")
    t._l._l = AVLTree(10, "d")
    t._l._r = AVLTree(30, "e")
    assert t.get(15) is None


@pytest.mark.get
def test_get_from_right_exists() -> None:
    """Test getting value from right that exists."""
    t = AVLTree(10, "a")
    t._r = AVLTree(15, "b")
    assert t.get(15) == "b"


@pytest.mark.get
def test_get_from_right_not_exists() -> None:
    """Test getting value from right that doesn't exist."""
    t = AVLTree(10, "a")
    t._r = AVLTree(15, "b")
    assert t.get(20) is None


@pytest.mark.get
def test_get_from_right_left_exists() -> None:
    """Test getting value from right-left that exists."""
    t = AVLTree(20, "a")
    t._l = AVLTree(10, "c")
    t._r = AVLTree(40, "b")
    t._r._l = AVLTree(30, "d")
    t._r._r = AVLTree(50, "e")
    assert t.get(30) == "d"


@pytest.mark.get
def test_get_from_right_left_not_exists() -> None:
    """Test getting value from right-left that doesn't exist."""
    t = AVLTree(20, "a")
    t._l = AVLTree(10, "c")
    t._r = AVLTree(40, "b")
    t._r._l = AVLTree(30, "d")
    t._r._r = AVLTree(50, "e")
    assert t.get(25) is None


@pytest.mark.get
def test_get_from_right_right_exists() -> None:
    """Test getting value from right-right that exists."""
    t = AVLTree(20, "a")
    t._l = AVLTree(10, "b")
    t._r = AVLTree(30, "c")
    t._r._r = AVLTree(40, "d")
    assert t.get(40) == "d"


@pytest.mark.get
def test_get_from_right_right_not_exists() -> None:
    """Test getting value from right-right that doesn't exist."""
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
def test_find_root_exists() -> None:
    """Test finding root that exists."""
    t = AVLTree(10, "a")
    assert t.find(10) is True


@pytest.mark.find
def test_find_root_not_exists() -> None:
    """Test finding root that doesn't exist."""
    t = AVLTree()
    assert t.find(5) is False


@pytest.mark.find
def test_find_left_exists() -> None:
    """Test finding left node that exists."""
    t = AVLTree(10, "a")
    t._l = AVLTree(5, "b")
    assert t.find(5) is True


@pytest.mark.find
def test_find_left_not_exists() -> None:
    """Test finding left node that doesn't exist."""
    t = AVLTree(10, "a")
    t._l = AVLTree(5, "b")
    assert t.find(3) is False


@pytest.mark.find
def test_find_left_left_exists() -> None:
    """Test finding left-left node that exists."""
    t = AVLTree(40, "a")
    t._l = AVLTree(20, "b")
    t._r = AVLTree(60, "c")
    t._l._l = AVLTree(10, "d")
    assert t.find(10) is True


@pytest.mark.find
def test_find_left_left_not_exists() -> None:
    """Test finding left-left node that doesn't exist."""
    t = AVLTree(40, "a")
    t._l = AVLTree(20, "b")
    t._r = AVLTree(60, "c")
    t._l._l = AVLTree(10, "d")
    assert t.find(5) is False


@pytest.mark.find
def test_find_left_right_exists() -> None:
    """Test finding left-right node that exists."""
    t = AVLTree(40, "a")
    t._l = AVLTree(20, "b")
    t._r = AVLTree(60, "c")
    t._l._l = AVLTree(10, "d")
    t._l._r = AVLTree(30, "e")
    assert t.find(30) is True


@pytest.mark.find
def test_find_left_right_not_exists() -> None:
    """Test finding left-right node that doesn't exist."""
    t = AVLTree(40, "a")
    t._l = AVLTree(20, "b")
    t._r = AVLTree(60, "c")
    t._l._l = AVLTree(10, "d")
    t._l._r = AVLTree(30, "e")
    assert t.find(15) is False


@pytest.mark.find
def test_find_right_exists() -> None:
    """Test finding right node that exists."""
    t = AVLTree(10, "a")
    t._r = AVLTree(15, "b")
    assert t.find(15) is True


@pytest.mark.find
def test_find_right_not_exists() -> None:
    """Test finding right node that doesn't exist."""
    t = AVLTree(10, "a")
    t._r = AVLTree(15, "b")
    assert t.find(20) is False


@pytest.mark.find
def test_find_right_left_exists() -> None:
    """Test finding right-left node that exists."""
    t = AVLTree(20, "a")
    t._l = AVLTree(10, "c")
    t._r = AVLTree(40, "b")
    t._r._l = AVLTree(30, "d")
    t._r._r = AVLTree(50, "e")
    assert t.find(30) is True


@pytest.mark.find
def test_find_right_left_not_exists() -> None:
    """Test finding right-left node that doesn't exist."""
    t = AVLTree(20, "a")
    t._l = AVLTree(10, "c")
    t._r = AVLTree(40, "b")
    t._r._l = AVLTree(30, "d")
    t._r._r = AVLTree(50, "e")
    assert t.find(25) is False


@pytest.mark.find
def test_find_right_right_exists() -> None:
    """Test finding right-right node that exists."""
    t = AVLTree(20, "a")
    t._l = AVLTree(10, "b")
    t._r = AVLTree(30, "c")
    t._r._r = AVLTree(40, "d")
    assert t.find(40) is True


@pytest.mark.find
def test_find_right_right_not_exists() -> None:
    """Test finding right-right node that doesn't exist."""
    t = AVLTree(20, "a")
    t._l = AVLTree(10, "b")
    t._r = AVLTree(30, "c")
    t._r._r = AVLTree(40, "d")
    assert t.find(35) is False


# ==================== 5. delete(x: int) ====================

@pytest.mark.delete
def test_delete_root_no_rebalance() -> None:
    """Test deleting root without rebalancing needed."""
    left = AVLTree(5, "b")
    t = AVLTree(10, "a")
    t._l = left
    t = t.delete(10)
    _assert_balanced(t)
    assert t._key == 5
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
    left = AVLTree(10, "b")
    right = AVLTree(40, "c")
    t = AVLTree(30, "a")
    t._l = left
    t._r = right
    t = t.delete(10)
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
    left = AVLTree(10, "b")
    t = AVLTree(30, "a")
    t._l = left
    t = t.delete(5)
    _assert_balanced(t)
    assert t._key == 30
    assert t._l._key == 10
    assert t._r is None


@pytest.mark.delete
def test_delete_left_non_leaf() -> None:
    """Test deleting non-leaf node from left."""
    left_left = AVLTree(20, "c")
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
        assert t._l._l._key == 20
        assert t._l._r is None or t._l._r._key is None
    else:
        assert t._l._key == 20
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
    t = AVLTree(10, "a")
    t._r = right
    t = t.delete(15)
    _assert_balanced(t)
    assert t._key == 10
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
def test_delete_right_non_leaf() -> None:
    """Test deleting non-leaf node from right."""
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
    left_right = AVLTree(25, "j")
    left = AVLTree(20, "d")
    left._l = left_left
    left._r = left_right
    right_left_left = AVLTree(35, "k")
    right_left_right = AVLTree(45, "l")
    right_left = AVLTree(40, "e")
    right_left._l = right_left_left
    right_left._r = right_left_right
    right_right_left = AVLTree(60, "f")
    right_right_right = AVLTree(80, "g")
    right_right = AVLTree(70, "c")
    right_right._l = right_right_left
    right_right._r = right_right_right
    right = AVLTree(50, "a")
    right._l = right_left
    right._r = right_right
    t = AVLTree(30, "b")
    t._l = left
    t._r = right
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
    t = AVLTree(5, "a")
    assert t.items() == [(5, "a")]


@pytest.mark.items
def test_items_two_nodes_ascending() -> None:
    """Test items() with two nodes inserted in ascending order."""
    right = AVLTree(2, "b")
    t = AVLTree(1, "a")
    t._r = right
    assert t.items() == [(1, "a"), (2, "b")]


@pytest.mark.items
def test_items_two_nodes_descending() -> None:
    """Test items() with two nodes inserted in descending order."""
    left = AVLTree(1, "b")
    t = AVLTree(2, "a")
    t._l = left
    assert t.items() == [(1, "b"), (2, "a")]


@pytest.mark.items
def test_items_three_nodes_ascending() -> None:
    """Test items() with three nodes inserted in ascending order."""
    right_right = AVLTree(3, "c")
    right = AVLTree(2, "b")
    right._r = right_right
    t = AVLTree(1, "a")
    t._r = right
    assert t.items() == [(1, "a"), (2, "b"), (3, "c")]


@pytest.mark.items
def test_items_three_nodes_descending() -> None:
    """Test items() with three nodes inserted in descending order."""
    left_left = AVLTree(1, "c")
    left = AVLTree(2, "b")
    left._l = left_left
    t = AVLTree(3, "a")
    t._l = left
    assert t.items() == [(1, "c"), (2, "b"), (3, "a")]


@pytest.mark.items
def test_items_three_nodes_mixed() -> None:
    """Test items() with three nodes inserted in mixed order."""
    left = AVLTree(1, "b")
    right = AVLTree(3, "c")
    t = AVLTree(2, "a")
    t._l = left
    t._r = right
    assert t.items() == [(1, "b"), (2, "a"), (3, "c")]
