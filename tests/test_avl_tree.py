from avltree import AVLTree


def test_set_and_items_sorted() -> None:
    tree = AVLTree()
    for key in [10, 5, 15, 3, 7, 12, 18]:
        tree = tree.set(key, str(key))

    assert tree.items() == [
        (3, "3"),
        (5, "5"),
        (7, "7"),
        (10, "10"),
        (12, "12"),
        (15, "15"),
        (18, "18"),
    ]


def test_get_and_find() -> None:
    tree = AVLTree()
    tree = tree.set(2, "a")
    tree = tree.set(1, "b")
    tree = tree.set(3, "c")

    assert tree.find(2) is True
    assert tree.find(4) is False
    assert tree.get(1) == "b"
    assert tree.get(4, "missing") == "missing"


def test_set_updates_value() -> None:
    tree = AVLTree()
    tree = tree.set(5, "a")
    tree = tree.set(5, "b")

    assert tree.get(5) == "b"
    assert tree.items() == [(5, "b")]


def test_delete_leaf_and_root() -> None:
    tree = AVLTree()
    tree = tree.set(2, "a")
    tree = tree.set(1, "b")
    tree = tree.set(3, "c")

    tree = tree.delete(1)
    assert tree.items() == [(2, "a"), (3, "c")]

    tree = tree.delete(2)
    assert tree.items() == [(3, "c")]


def test_delete_last_node_returns_empty_tree() -> None:
    tree = AVLTree()
    tree = tree.set(1, "a")

    tree = tree.delete(1)
    assert tree.items() == []
