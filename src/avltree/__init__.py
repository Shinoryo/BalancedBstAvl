"""AVL tree library."""

from importlib.metadata import PackageNotFoundError, version

from .avl_tree import AVLTree

__all__ = ["AVLTree"]

try:
    __version__ = version("BalancedBstAvl")
except PackageNotFoundError:
    # Fallback for editable/dev environments before installation.
    __version__ = "0.0.0"
