"""AVL tree (self-balancing binary search tree) implementation."""

from __future__ import annotations

from typing import Any


class AVLTree:
    """Implementation of a Binary Search Tree (AVL tree).

    An empty tree is represented by a node with ``_key`` set to ``None``.

    Attributes:
        _key (int | None): The node's key. None if the node is empty.
        _value: The value associated with the key.
        _l (AVLTree | None): The left child node.
        _r (AVLTree | None): The right child node.
        _h (int): The height of the node. 0 if the node is empty.
    """

    def __init__(self, key: int | None = None, value: Any = None) -> None:
        """Initialize an AVLTree node.

        Args:
            key (int | None, optional): The key to store in the node. If None,
                the node becomes empty (default: None).
            value: The associated value (default: None).
        """
        self._key = key
        self._value = value
        self._l = None
        self._r = None
        if key is not None:
            self._h = 1
        else:
            self._h = 0

    def delete(self, x: int) -> AVLTree:
        """Delete key x from the tree.

        If the key does not exist, the tree remains unchanged.

        Args:
            x (int): The key to delete.

        Returns:
            AVLTree: The root node of the balanced tree.
        """
        if self._key is None:
            return self

        if x < self._key:
            if self._l is not None:
                result = self._l.delete(x)
                # Empty node should not be stored as a child
                self._l = result if result._key is not None else None
        elif x > self._key:
            if self._r is not None:
                result = self._r.delete(x)
                # Empty node should not be stored as a child
                self._r = result if result._key is not None else None
        else:  # x == self._key
            if self._l is None:
                return self._r if self._r is not None else AVLTree()
            if self._r is None:
                return self._l
            # Two children case: find successor (minimum in right subtree)
            t = self._r
            while t._l is not None:
                t = t._l
            self._key = t._key
            self._value = t._value
            result = self._r.delete(t._key)
            # Empty node should not be stored as a child
            self._r = result if result._key is not None else None

        return self._balance()

    def find(self, x: int) -> bool:
        """Check if key x is in the tree.

        Args:
            x (int): The key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
        """
        if self._key is None:
            return False
        if x == self._key:
            return True
        if x < self._key:
            return self._l.find(x) if self._l else False
        return self._r.find(x) if self._r else False

    def get(self, x: int, default: Any = None) -> Any:
        """Retrieve the value associated with key x.

        Args:
            x (int): The key to search for.
            default: The default value if the key is not found (default: None).

        Returns:
            The value if the key is found, otherwise the default value.
        """
        if self._key is None:
            return default
        if x == self._key:
            return self._value
        if x < self._key:
            return self._l.get(x, default) if self._l else default
        return self._r.get(x, default) if self._r else default

    def items(self) -> list[tuple[int, Any]]:
        """Return all (key, value) pairs in the tree in ascending key order.

        Returns:
            list: A list of (key, value) tuples, sorted by key.
        """
        result = []
        self._inorder_traverse(result)
        return result

    def set(self, x: int, value: Any) -> AVLTree:
        """Update the value associated with key x.

        If the key does not exist, it is inserted.

        Args:
            x (int): The key to update.
            value: The value to set.

        Returns:
            AVLTree: The root node of the balanced tree.
        """
        if self._key is None:
            self._key = x
            self._value = value
            self._h = 1
            return self
        if x < self._key:
            if self._l:
                self._l = self._l.set(x, value)
            else:
                self._l = AVLTree(x, value)
        elif x > self._key:
            if self._r:
                self._r = self._r.set(x, value)
            else:
                self._r = AVLTree(x, value)
        else:
            self._value = value
        return self._balance()

    def _height(self, t: AVLTree | None) -> int:
        """Return the height of node t.

        Args:
            t (AVLTree | None): The target node.

        Returns:
            int: The height of the node. Returns 0 if the node is None.
        """
        if t is None or t._key is None:
            return 0
        return t._h

    def _update(self) -> None:
        """Update the height of this node.

        Recalculates the height based on the heights of the left and right children.
        """
        if self._key is None:
            self._h = 0
            return
        self._h = max(self._height(self._l), self._height(self._r)) + 1

    def _bf(self) -> int:
        """Calculate the balance factor of this node.

        Returns:
            int: The difference between the height of the left and right subtrees.
        """
        return self._height(self._l) - self._height(self._r)

    def _rot_r(self) -> AVLTree:
        """Rotate right (left child becomes the new root).

        Returns:
            AVLTree: The new root node after rotation.
        """
        t = self._l
        self._l = t._r
        t._r = self
        self._update()
        t._update()
        return t

    def _rot_l(self) -> AVLTree:
        """Rotate left (right child becomes the new root).

        Returns:
            AVLTree: The new root node after rotation.
        """
        t = self._r
        self._r = t._l
        t._l = self
        self._update()
        t._update()
        return t

    def _inorder_traverse(self, result: list[tuple[int, Any]]) -> None:
        """Add all nodes to the list using in-order traversal.

        Args:
            result (list): The list to store the traversal results.
        """
        if self._key is None:
            return
        if self._l:
            self._l._inorder_traverse(result)
        result.append((self._key, self._value))
        if self._r:
            self._r._inorder_traverse(result)

    def _balance(self) -> AVLTree:
        """Balance this node.

        Returns:
            AVLTree: The balanced node.
        """
        if self._key is None:
            return self
        self._update()

        if self._bf() > 1:
            if self._l and self._l._bf() < 0:
                self._l = self._l._rot_l()
            return self._rot_r()

        if self._bf() < -1:
            if self._r and self._r._bf() > 0:
                self._r = self._r._rot_r()
            return self._rot_l()

        return self
