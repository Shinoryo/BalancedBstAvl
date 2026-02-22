import pytest

from avltree import AVLTree

# ==================== 1. __init__ (Constructor) ====================

@pytest.mark.init
def test_init_empty():
    """Test AVLTree() creates empty tree with all attributes set to defaults."""
    t = AVLTree()
    assert t._key is None
    assert t._value is None
    assert t._h == 0
    assert t._l is None
    assert t._r is None


@pytest.mark.init
def test_init_with_key():
    """Test AVLTree(10) creates tree with key, height=1, value=None."""
    t = AVLTree(10)
    assert t._key == 10
    assert t._value is None
    assert t._h == 1
    assert t._l is None
    assert t._r is None


@pytest.mark.init
def test_init_with_key_and_value():
    """Test AVLTree(5, 'val') creates tree with key and value."""
    t = AVLTree(5, "val")
    assert t._key == 5
    assert t._value == "val"
    assert t._h == 1


# ==================== 2. set(x: int, value: Any) ====================

@pytest.mark.set
def test_set_to_empty_tree():
    """Test adding a node to an empty tree."""
    t = AVLTree()
    t.set(5, "a")
    assert t._key == 5
    assert t._value == "a"


@pytest.mark.set
def test_set_update_root():
    """Test updating the root node."""
    t = AVLTree()
    t.set(5, "old")
    t.set(5, "new")
    assert t._key == 5
    assert t._value == "new"


@pytest.mark.set
def test_set_insert_left():
    """Test inserting a node to the left of root."""
    t = AVLTree()
    t.set(10, "a")
    t.set(5, "b")
    assert t._key == 10
    assert t._l._key == 5
    assert t._l._value == "b"


@pytest.mark.set
def test_set_update_left():
    """Test updating a node to the left of root."""
    t = AVLTree()
    t.set(10, "a")
    t.set(5, "b")
    t.set(5, "b_new")
    assert t._l._value == "b_new"


@pytest.mark.set
def test_set_left_left_no_rebalance():
    """Test inserting a node to the left-left without rebalancing."""
    t = AVLTree()
    t.set(50, "a")
    t.set(30, "b")
    t.set(70, "c")
    t.set(60, "d")
    t.set(20, "f")
    assert t.items() == [(20, "f"), (30, "b"), (50, "a"), (60, "d"), (70, "c")]


@pytest.mark.set
def test_set_left_left_with_rebalance():
    """Test inserting a node to the left-left with rebalancing."""
    t = AVLTree()
    t.set(10, "a")
    t.set(5, "b")
    t.set(3, "c")
    items = t.items()
    assert items == [(3, "c"), (5, "b"), (10, "a")]
    assert all(items[i][0] <= items[i+1][0] for i in range(len(items)-1))


@pytest.mark.set
def test_set_update_left_left():
    """Test updating a node to the left-left of root."""
    t = AVLTree()
    t.set(50, "a")
    t.set(30, "b")
    t.set(70, "c")
    t.set(60, "d")
    t.set(20, "d")
    t.set(20, "d_new")
    assert t._l._l._value == "d_new"


@pytest.mark.set
def test_set_left_right_no_rebalance():
    """Test inserting a node to the left-right without rebalancing."""
    t = AVLTree()
    t.set(20, "a")
    t.set(10, "b")
    t.set(30, "c")
    assert t.items() == [(10, "b"), (20, "a"), (30, "c")]


@pytest.mark.set
def test_set_left_right_with_rebalance():
    """Test inserting a node to the left-right with rebalancing."""
    t = AVLTree()
    t.set(10, "a")
    t.set(3, "b")
    t.set(5, "c")
    items = t.items()
    assert items == [(3, "b"), (5, "c"), (10, "a")]
    assert all(items[i][0] <= items[i+1][0] for i in range(len(items)-1))


@pytest.mark.set
def test_set_update_left_right():
    """Test updating a node to the left-right of root."""
    t = AVLTree()
    t.set(20, "a")
    t.set(10, "b")
    t.set(30, "c")
    t.set(30, "c_new")
    assert t._r._value == "c_new"


@pytest.mark.set
def test_set_insert_right():
    """Test inserting a node to the right of root."""
    t = AVLTree()
    t.set(10, "a")
    t.set(15, "b")
    assert t._key == 10
    assert t._r._key == 15
    assert t._r._value == "b"


@pytest.mark.set
def test_set_update_right():
    """Test updating a node to the right of root."""
    t = AVLTree()
    t.set(10, "a")
    t.set(15, "b")
    t.set(15, "b_new")
    assert t._r._value == "b_new"


@pytest.mark.set
def test_set_right_left_no_rebalance():
    """Test inserting a node to the right-left without rebalancing."""
    t = AVLTree()
    t.set(20, "a")
    t.set(10, "b")
    t.set(40, "c")
    t.set(35, "d")
    assert t.items() == [(10, "b"), (20, "a"), (35, "d"), (40, "c")]


@pytest.mark.set
def test_set_right_left_with_rebalance():
    """Test inserting a node to the right-left with rebalancing."""
    t = AVLTree()
    t.set(30, "a")
    t.set(40, "b")
    t.set(35, "c")
    items = t.items()
    assert items == [(30, "a"), (35, "c"), (40, "b")]
    assert all(items[i][0] <= items[i+1][0] for i in range(len(items)-1))


@pytest.mark.set
def test_set_update_right_left():
    """Test updating a node to the right-left of root."""
    t = AVLTree()
    t.set(10, "a")
    t.set(30, "b")
    t.set(20, "c")
    t.set(20, "c_new")
    assert t._r._l._value == "c_new"


@pytest.mark.set
def test_set_right_right_no_rebalance():
    """Test inserting a node to the right-right without rebalancing."""
    t = AVLTree()
    t.set(20, "a")
    t.set(10, "b")
    t.set(25, "c")
    t.set(30, "d")
    assert t.items() == [(10, "b"), (20, "a"), (25, "c"), (30, "d")]


@pytest.mark.set
def test_set_right_right_with_rebalance():
    """Test inserting a node to the right-right with rebalancing."""
    t = AVLTree()
    t.set(30, "a")
    t.set(40, "b")
    t.set(50, "c")
    items = t.items()
    assert items == [(30, "a"), (40, "b"), (50, "c")]
    assert all(items[i][0] <= items[i+1][0] for i in range(len(items)-1))


@pytest.mark.set
def test_set_update_right_right():
    """Test updating a node to the right-right of root."""
    t = AVLTree()
    t.set(10, "a")
    t.set(20, "b")
    t.set(30, "c")
    t.set(30, "c_new")
    assert t._r._r._value == "c_new"


# ==================== 3. get(x: int, default=None) ====================

@pytest.mark.get
def test_get_from_root_exists():
    """Test getting value from root that exists."""
    t = AVLTree()
    t.set(10, "a")
    assert t.get(10) == "a"


@pytest.mark.get
def test_get_from_root_not_exists():
    """Test getting value from root that doesn't exist."""
    t = AVLTree()
    assert t.get(5) is None


@pytest.mark.get
def test_get_from_left_exists():
    """Test getting value from left that exists."""
    t = AVLTree()
    t.set(10, "a")
    t.set(5, "b")
    assert t.get(5) == "b"


@pytest.mark.get
def test_get_from_left_not_exists():
    """Test getting value from left that doesn't exist."""
    t = AVLTree()
    t.set(10, "a")
    t.set(5, "b")
    assert t.get(3) is None


@pytest.mark.get
def test_get_from_left_left_exists():
    """Test getting value from left-left that exists."""
    t = AVLTree()
    t.set(40, "a")
    t.set(20, "b")
    t.set(60, "c")
    t.set(10, "d")
    assert t.get(10) == "d"


@pytest.mark.get
def test_get_from_left_left_not_exists():
    """Test getting value from left-left that doesn't exist."""
    t = AVLTree()
    t.set(40, "a")
    t.set(20, "b")
    t.set(60, "c")
    t.set(10, "d")
    assert t.get(5) is None


@pytest.mark.get
def test_get_from_left_right_exists():
    """Test getting value from left-right that exists."""
    t = AVLTree()
    t.set(40, "a")
    t.set(20, "b")
    t.set(60, "c")
    t.set(10, "d")
    t.set(30, "e")
    assert t.get(30) == "e"


@pytest.mark.get
def test_get_from_left_right_not_exists():
    """Test getting value from left-right that doesn't exist."""
    t = AVLTree()
    t.set(40, "a")
    t.set(20, "b")
    t.set(60, "c")
    t.set(10, "d")
    t.set(30, "e")
    assert t.get(15) is None


@pytest.mark.get
def test_get_from_right_exists():
    """Test getting value from right that exists."""
    t = AVLTree()
    t.set(10, "a")
    t.set(15, "b")
    assert t.get(15) == "b"


@pytest.mark.get
def test_get_from_right_not_exists():
    """Test getting value from right that doesn't exist."""
    t = AVLTree()
    t.set(10, "a")
    t.set(15, "b")
    assert t.get(20) is None


@pytest.mark.get
def test_get_from_right_left_exists():
    """Test getting value from right-left that exists."""
    t = AVLTree()
    t.set(20, "a")
    t.set(40, "b")
    t.set(10, "c")
    t.set(30, "d")
    t.set(50, "e")
    assert t.get(30) == "d"


@pytest.mark.get
def test_get_from_right_left_not_exists():
    """Test getting value from right-left that doesn't exist."""
    t = AVLTree()
    t.set(20, "a")
    t.set(40, "b")
    t.set(10, "c")
    t.set(30, "d")
    t.set(50, "e")
    assert t.get(25) is None


@pytest.mark.get
def test_get_from_right_right_exists():
    """Test getting value from right-right that exists."""
    t = AVLTree()
    t.set(20, "a")
    t.set(10, "b")
    t.set(30, "c")
    t.set(40, "d")
    assert t.get(40) == "d"


@pytest.mark.get
def test_get_from_right_right_not_exists():
    """Test getting value from right-right that doesn't exist."""
    t = AVLTree()
    t.set(20, "a")
    t.set(10, "b")
    t.set(30, "c")
    t.set(40, "d")
    assert t.get(35) is None


@pytest.mark.get
def test_get_default_not_specified():
    """Test get with default value not specified."""
    t = AVLTree()
    assert t.get(5) is None


@pytest.mark.get
def test_get_default_specified():
    """Test get with default value specified."""
    t = AVLTree()
    assert t.get(5, "default") == "default"


# ==================== 4. find(x: int) ====================

@pytest.mark.find
def test_find_root_exists():
    """Test finding root that exists."""
    t = AVLTree()
    t.set(10, "a")
    assert t.find(10) is True


@pytest.mark.find
def test_find_root_not_exists():
    """Test finding root that doesn't exist."""
    t = AVLTree()
    assert t.find(5) is False


@pytest.mark.find
def test_find_left_exists():
    """Test finding left node that exists."""
    t = AVLTree()
    t.set(10, "a")
    t.set(5, "b")
    assert t.find(5) is True


@pytest.mark.find
def test_find_left_not_exists():
    """Test finding left node that doesn't exist."""
    t = AVLTree()
    t.set(10, "a")
    t.set(5, "b")
    assert t.find(3) is False


@pytest.mark.find
def test_find_left_left_exists():
    """Test finding left-left node that exists."""
    t = AVLTree()
    t.set(40, "a")
    t.set(20, "b")
    t.set(60, "c")
    t.set(10, "d")
    assert t.find(10) is True


@pytest.mark.find
def test_find_left_left_not_exists():
    """Test finding left-left node that doesn't exist."""
    t = AVLTree()
    t.set(40, "a")
    t.set(20, "b")
    t.set(60, "c")
    t.set(10, "d")
    assert t.find(5) is False


@pytest.mark.find
def test_find_left_right_exists():
    """Test finding left-right node that exists."""
    t = AVLTree()
    t.set(40, "a")
    t.set(20, "b")
    t.set(60, "c")
    t.set(10, "d")
    t.set(30, "e")
    assert t.find(30) is True


@pytest.mark.find
def test_find_left_right_not_exists():
    """Test finding left-right node that doesn't exist."""
    t = AVLTree()
    t.set(40, "a")
    t.set(20, "b")
    t.set(60, "c")
    t.set(10, "d")
    t.set(30, "e")
    assert t.find(15) is False


@pytest.mark.find
def test_find_right_exists():
    """Test finding right node that exists."""
    t = AVLTree()
    t.set(10, "a")
    t.set(15, "b")
    assert t.find(15) is True


@pytest.mark.find
def test_find_right_not_exists():
    """Test finding right node that doesn't exist."""
    t = AVLTree()
    t.set(10, "a")
    t.set(15, "b")
    assert t.find(20) is False


@pytest.mark.find
def test_find_right_left_exists():
    """Test finding right-left node that exists."""
    t = AVLTree()
    t.set(20, "a")
    t.set(40, "b")
    t.set(10, "c")
    t.set(30, "d")
    t.set(50, "e")
    assert t.find(30) is True


@pytest.mark.find
def test_find_right_left_not_exists():
    """Test finding right-left node that doesn't exist."""
    t = AVLTree()
    t.set(20, "a")
    t.set(40, "b")
    t.set(10, "c")
    t.set(30, "d")
    t.set(50, "e")
    assert t.find(25) is False


@pytest.mark.find
def test_find_right_right_exists():
    """Test finding right-right node that exists."""
    t = AVLTree()
    t.set(20, "a")
    t.set(10, "b")
    t.set(30, "c")
    t.set(40, "d")
    assert t.find(40) is True


@pytest.mark.find
def test_find_right_right_not_exists():
    """Test finding right-right node that doesn't exist."""
    t = AVLTree()
    t.set(20, "a")
    t.set(10, "b")
    t.set(30, "c")
    t.set(40, "d")
    assert t.find(35) is False


# ==================== 5. delete(x: int) ====================

@pytest.mark.delete
def test_delete_root_no_rebalance():
    """Test deleting root without rebalancing needed."""
    t = AVLTree()
    t.set(10, "a")
    t.set(5, "b")
    t.delete(10)
    assert t.items() == [(5, "b")]


@pytest.mark.delete
def test_delete_root_with_rebalance():
    """Test deleting root with rebalancing needed."""
    t = AVLTree()
    t.set(40, "a")
    t.set(20, "b")
    t.set(60, "c")
    t.set(10, "d")
    t.set(5, "e")
    t.delete(60)
    items = t.items()
    assert all(items[i][0] <= items[i+1][0] for i in range(len(items)-1))


@pytest.mark.delete
def test_delete_root_not_found():
    """Test deleting from root when target not found."""
    t = AVLTree()
    original_items = t.items()
    t.delete(5)
    assert t.items() == original_items


@pytest.mark.delete
def test_delete_root_leaf():
    """Test deleting root when it's a leaf."""
    t = AVLTree()
    t.set(5, "a")
    t.delete(5)
    assert t.items() == []


@pytest.mark.delete
def test_delete_left_no_rebalance():
    """Test deleting from left without rebalancing needed."""
    t = AVLTree()
    t.set(30, "a")
    t.set(10, "b")
    t.set(40, "c")
    t.delete(10)
    assert 10 not in [item[0] for item in t.items()]


@pytest.mark.delete
def test_delete_left_with_rebalance():
    """Test deleting from left with rebalancing needed."""
    t = AVLTree()
    t.set(50, "a")
    t.set(30, "b")
    t.set(70, "c")
    t.set(20, "d")
    t.set(10, "e")
    t.delete(70)
    items = t.items()
    assert all(items[i][0] <= items[i+1][0] for i in range(len(items)-1))


@pytest.mark.delete
def test_delete_left_not_found():
    """Test deleting from left when target not found."""
    t = AVLTree()
    t.set(30, "a")
    t.set(10, "b")
    original_items = t.items()
    t.delete(5)
    assert t.items() == original_items


@pytest.mark.delete
def test_delete_left_non_leaf():
    """Test deleting non-leaf node from left."""
    t = AVLTree()
    t.set(50, "a")
    t.set(30, "b")
    t.set(20, "c")
    t.set(40, "d")
    t.delete(30)
    items = t.items()
    assert 30 not in [item[0] for item in items]


@pytest.mark.delete
def test_delete_left_left_no_rebalance():
    """Test deleting from left-left without rebalancing needed."""
    t = AVLTree()
    t.set(40, "a")
    t.set(20, "b")
    t.set(60, "c")
    t.set(10, "d")
    t.delete(10)
    assert 10 not in [item[0] for item in t.items()]


@pytest.mark.delete
def test_delete_left_left_with_rebalance():
    """Test deleting from left-left with rebalancing needed."""
    t = AVLTree()
    t.set(60, "a")
    t.set(40, "b")
    t.set(80, "c")
    t.set(30, "d")
    t.set(20, "e")
    t.delete(80)
    items = t.items()
    assert all(items[i][0] <= items[i+1][0] for i in range(len(items)-1))


@pytest.mark.delete
def test_delete_left_left_not_found():
    """Test deleting from left-left when target not found."""
    t = AVLTree()
    t.set(40, "a")
    t.set(20, "b")
    original_items = t.items()
    t.delete(5)
    assert t.items() == original_items


@pytest.mark.delete
def test_delete_left_right_no_rebalance():
    """Test deleting from left-right without rebalancing needed."""
    t = AVLTree()
    t.set(40, "a")
    t.set(20, "b")
    t.set(60, "c")
    t.set(10, "d")
    t.set(30, "e")
    t.delete(30)
    assert 30 not in [item[0] for item in t.items()]


@pytest.mark.delete
def test_delete_left_right_with_rebalance():
    """Test deleting from left-right with rebalancing needed."""
    t = AVLTree()
    t.set(50, "a")
    t.set(30, "b")
    t.set(70, "c")
    t.set(20, "d")
    t.set(10, "e")
    t.set(25, "f")
    t.delete(70)
    items = t.items()
    assert all(items[i][0] <= items[i+1][0] for i in range(len(items)-1))


@pytest.mark.delete
def test_delete_left_right_not_found():
    """Test deleting from left-right when target not found."""
    t = AVLTree()
    t.set(40, "a")
    t.set(20, "b")
    t.set(60, "c")
    original_items = t.items()
    t.delete(15)
    assert t.items() == original_items


@pytest.mark.delete
def test_delete_right_no_rebalance():
    """Test deleting from right without rebalancing needed."""
    t = AVLTree()
    t.set(10, "a")
    t.set(15, "b")
    t.delete(15)
    assert t.items() == [(10, "a")]


@pytest.mark.delete
def test_delete_right_with_rebalance():
    """Test deleting from right with rebalancing needed."""
    t = AVLTree()
    t.set(20, "a")
    t.set(10, "b")
    t.set(30, "c")
    t.set(40, "d")
    t.set(50, "e")
    t.delete(10)
    items = t.items()
    assert all(items[i][0] <= items[i+1][0] for i in range(len(items)-1))


@pytest.mark.delete
def test_delete_right_not_found():
    """Test deleting from right when target not found."""
    t = AVLTree()
    t.set(10, "a")
    t.set(15, "b")
    original_items = t.items()
    t.delete(20)
    assert t.items() == original_items


@pytest.mark.delete
def test_delete_right_non_leaf():
    """Test deleting non-leaf node from right."""
    t = AVLTree()
    t.set(40, "a")
    t.set(20, "b")
    t.set(60, "c")
    t.set(50, "d")
    t.delete(50)
    items = t.items()
    assert 50 not in [item[0] for item in items]


@pytest.mark.delete
def test_delete_right_left_no_rebalance():
    """Test deleting from right-left without rebalancing needed."""
    t = AVLTree()
    t.set(20, "a")
    t.set(40, "b")
    t.set(10, "c")
    t.set(30, "d")
    t.set(50, "e")
    t.delete(30)
    assert 30 not in [item[0] for item in t.items()]


@pytest.mark.delete
def test_delete_right_left_with_rebalance():
    """Test deleting from right-left with rebalancing needed."""
    t = AVLTree()
    t.set(30, "a")
    t.set(10, "b")
    t.set(50, "c")
    t.set(5, "d")
    t.set(15, "e")
    t.set(12, "f")
    t.delete(5)
    items = t.items()
    assert all(items[i][0] <= items[i+1][0] for i in range(len(items)-1))


@pytest.mark.delete
def test_delete_right_left_not_found():
    """Test deleting from right-left when target not found."""
    t = AVLTree()
    t.set(20, "a")
    t.set(40, "b")
    t.set(10, "c")
    original_items = t.items()
    t.delete(25)
    assert t.items() == original_items


@pytest.mark.delete
def test_delete_right_right_no_rebalance():
    """Test deleting from right-right without rebalancing needed."""
    t = AVLTree()
    t.set(20, "a")
    t.set(10, "b")
    t.set(30, "c")
    t.set(40, "d")
    t.delete(40)
    assert 40 not in [item[0] for item in t.items()]


@pytest.mark.delete
def test_delete_right_right_with_rebalance():
    """Test deleting from right-right with rebalancing needed."""
    t = AVLTree()
    t.set(10, "a")
    t.set(20, "b")
    t.set(30, "c")
    t.set(40, "d")
    t.set(50, "e")
    t.delete(20)
    items = t.items()
    assert all(items[i][0] <= items[i+1][0] for i in range(len(items)-1))


@pytest.mark.delete
def test_delete_right_right_not_found():
    """Test deleting from right-right when target not found."""
    t = AVLTree()
    t.set(20, "a")
    t.set(10, "b")
    t.set(30, "c")
    original_items = t.items()
    t.delete(35)
    assert t.items() == original_items


@pytest.mark.delete
def test_delete_2child_successor_is_leaf():
    """Test deleting 2-child node where successor is leaf."""
    t = AVLTree()
    t.set(30, "a")
    t.set(10, "b")
    t.set(50, "c")
    t.set(5, "d")
    t.set(20, "e")
    t.set(40, "f")
    t.set(60, "g")
    t.delete(30)
    items = t.items()
    assert 30 not in [item[0] for item in items]
    assert all(items[i][0] <= items[i+1][0] for i in range(len(items)-1))


@pytest.mark.delete
def test_delete_2child_successor_has_right_child():
    """Test deleting 2-child node where successor has right child."""
    t = AVLTree()
    t.set(30, "a")
    t.set(20, "b")
    t.set(40, "c")
    t.set(35, "d")
    t.set(37, "e")
    t.set(50, "f")
    t.delete(30)
    items = t.items()
    assert 30 not in [item[0] for item in items]
    assert all(items[i][0] <= items[i+1][0] for i in range(len(items)-1))


@pytest.mark.delete
def test_delete_2child_with_rebalance():
    """Test deleting 2-child node with rebalancing after replacement."""
    t = AVLTree()
    t.set(50, "a")
    t.set(30, "b")
    t.set(70, "c")
    t.set(20, "d")
    t.set(40, "e")
    t.set(60, "f")
    t.set(80, "g")
    t.set(10, "h")
    t.set(5, "i")
    t.set(25, "j")
    t.set(35, "k")
    t.set(45, "l")
    t.delete(30)
    items = t.items()
    assert 30 not in [item[0] for item in items]
    assert all(items[i][0] <= items[i+1][0] for i in range(len(items)-1))


# ==================== 6. items() ====================

@pytest.mark.items
def test_items_empty_tree():
    """Test items() on empty tree."""
    t = AVLTree()
    assert t.items() == []


@pytest.mark.items
def test_items_single_node():
    """Test items() with single node."""
    t = AVLTree()
    t.set(5, "a")
    assert t.items() == [(5, "a")]


@pytest.mark.items
def test_items_two_nodes_ascending():
    """Test items() with two nodes inserted in ascending order."""
    t = AVLTree()
    t.set(1, "a")
    t.set(2, "b")
    assert t.items() == [(1, "a"), (2, "b")]


@pytest.mark.items
def test_items_two_nodes_descending():
    """Test items() with two nodes inserted in descending order."""
    t = AVLTree()
    t.set(2, "a")
    t.set(1, "b")
    assert t.items() == [(1, "b"), (2, "a")]


@pytest.mark.items
def test_items_three_nodes_ascending():
    """Test items() with three nodes inserted in ascending order."""
    t = AVLTree()
    t.set(1, "a")
    t.set(2, "b")
    t.set(3, "c")
    assert t.items() == [(1, "a"), (2, "b"), (3, "c")]


@pytest.mark.items
def test_items_three_nodes_descending():
    """Test items() with three nodes inserted in descending order."""
    t = AVLTree()
    t.set(3, "a")
    t.set(2, "b")
    t.set(1, "c")
    assert t.items() == [(1, "c"), (2, "b"), (3, "a")]


@pytest.mark.items
def test_items_three_nodes_mixed():
    """Test items() with three nodes inserted in mixed order."""
    t = AVLTree()
    t.set(2, "a")
    t.set(1, "b")
    t.set(3, "c")
    assert t.items() == [(1, "b"), (2, "a"), (3, "c")]
