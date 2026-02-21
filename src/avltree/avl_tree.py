"""AVL tree (self-balancing binary search tree) implementation."""

from __future__ import annotations

from typing import Any


class AVLTree:
    """二分探索木(AVL木)の実装。

    Attributes:
        _key (int): ノードの値.
        _value: キーに付随する値.
        _l (AVLTree): 左の子ノード.
        _r (AVLTree): 右の子ノード.
        _h (int): ノードの高さ.
    """

    def __init__(self, key: int | None = None, value: Any = None) -> None:
        """AVLTreeノードを初期化します.

        Args:
            key (int, optional): ノードに格納する値. Noneの場合、空のノードに
                なります (デフォルト: None).
            value: 付随する値 (デフォルト: None).
        """
        self._key = key
        self._value = value
        self._l = None
        self._r = None
        if key is not None:
            self._h = 1
        else:
            self._h = 0

    def insert(self, x: int, value: Any = None) -> AVLTree:
        """値xを木に挿入します.

        Args:
            x (int): 挿入する値.
            value: xに付随する値 (デフォルト: None).

        Returns:
            AVLTree: バランスが取られた木のルートノード.
        """
        if self._key is None:
            self._key = x
            self._value = value
            self._h = 1
            return self

        if x < self._key:
            if self._l:
                self._l = self._l.insert(x, value)
            else:
                self._l = AVLTree(x, value)
        elif x > self._key:
            if self._r:
                self._r = self._r.insert(x, value)
            else:
                self._r = AVLTree(x, value)
        return self._balance()

    def delete(self, x: int) -> AVLTree:
        """値xを木から削除します.

        Args:
            x (int): 削除する値.

        Returns:
            AVLTree: バランスが取られた木のルートノード.
        """
        if self._key is None:
            return self

        if x < self._key and self._l:
            self._l = self._l.delete(x)
        elif x > self._key and self._r:
            self._r = self._r.delete(x)
        elif x == self._key:
            if not self._l:
                if self._r is not None:
                    return self._r
                return AVLTree()
            if not self._r:
                if self._l is not None:
                    return self._l
                return AVLTree()
            t = self._r
            while t._l:
                t = t._l
            self._key = t._key
            self._value = t._value
            self._r = self._r.delete(t._key)

        return self._balance()

    def find(self, x: int) -> bool:
        """値xが木に含まれるか判定します.

        Args:
            x (int): 検索する値.

        Returns:
            bool: 値が見つかればTrue、見つからなければFalse.
        """
        if self._key is None:
            return False
        if x == self._key:
            return True
        if x < self._key:
            if self._l:
                return self._l.find(x)
            return False
        if self._r:
            return self._r.find(x)
        return False

    def get(self, x: int, default: Any = None) -> Any:
        """キーxに付随する値を取得します.

        Args:
            x (int): 検索するキー.
            default: キーが見つからない場合のデフォルト値 (デフォルト: None).

        Returns:
            キーが見つかればその値、見つからなければdefaultを返します.
        """
        if self._key is None:
            return default
        if x == self._key:
            return self._value
        if x < self._key:
            if self._l:
                return self._l.get(x, default)
            return default
        if self._r:
            return self._r.get(x, default)
        return default

    def set(self, x: int, value: Any) -> AVLTree:
        """キーxの付随する値を更新します.

        キーが存在しない場合は合わせて挿入します。

        Args:
            x (int): 更新するキー.
            value: 設定する値.

        Returns:
            AVLTree: バランスが取られた木のルートノード.
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
        """ノードtの高さを返します.

        Args:
            t (AVLTree or None): 対象のノード.

        Returns:
            int: ノードの高さ。ノードがNoneの場合は0.
        """
        if t:
            return t._h
        return 0

    def _update(self) -> None:
        """このノードの高さを更新します.

        左右の子ノードの高さから自分の高さを再計算します.
        """
        if self._key is None:
            self._h = 0
            return
        self._h = max(self._height(self._l), self._height(self._r)) + 1

    def _bf(self) -> int:
        """このノードのバランスファクターを計算します.

        Returns:
            int: 左部分木の高さと右部分木の高さの差.
        """
        return self._height(self._l) - self._height(self._r)

    def _rot_r(self) -> AVLTree:
        """右方向に回転します(左の子が新しいルートになります).

        Returns:
            AVLTree: 回転後の新しいルートノード.
        """
        t = self._l
        self._l = t._r
        t._r = self
        self._update()
        t._update()
        return t

    def _rot_l(self) -> AVLTree:
        """左方向に回転します(右の子が新しいルートになります).

        Returns:
            AVLTree: 回転後の新しいルートノード.
        """
        t = self._r
        self._r = t._l
        t._l = self
        self._update()
        t._update()
        return t

    def items(self) -> list[tuple[int, Any]]:
        """木に含まれるすべての(キー, 値)ペアをキーの昇順で返します.

        Returns:
            list: (キー, 値)のタプルのリスト、キー順でソート済み.
        """
        result = []
        self._inorder_traverse(result)
        return result

    def _inorder_traverse(self, result: list[tuple[int, Any]]) -> None:
        """中順走査で全ノードをリストに追加します(プライベートメソッド).

        Args:
            result (list): 走査結果を格納するリスト.
        """
        if self._key is None:
            return
        if self._l:
            self._l._inorder_traverse(result)
        result.append((self._key, self._value))
        if self._r:
            self._r._inorder_traverse(result)

    def _balance(self) -> AVLTree:
        """このノードをバランスさせます.

        Returns:
            AVLTree: バランスが取られたノード.
        """
        if self._key is None:
            return self
        self._update()

        if self._bf() > 1:
            if self._l._bf() < 0:
                self._l = self._l._rot_l()
            return self._rot_r()

        if self._bf() < -1:
            if self._r._bf() > 0:
                self._r = self._r._rot_r()
            return self._rot_l()

        return self
