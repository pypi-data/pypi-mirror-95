from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Union
from dekespo_ai_sdk.core.utils import error_print


class DisjointSet:
    @dataclass
    class Element:
        id_: Any
        rank: int = 0
        size: int = 1
        parent: Any = field(init=False)

        def __post_init__(self):
            self.parent = self

        def __str__(self):
            return f"Rank: {self.rank}, Id: {self.id_}, Size: {self.size}"

        def __repr__(self):  # pragma: no cover
            return self.__str__()

    def __init__(self):
        self._set = dict()

    def make_set(self, element: Element):
        if not self._is_element_id_in(element.id_):
            self._set[element.id_] = DisjointSet.Element(element.id_)
        else:
            error_print(
                f"Element id {element.id_} already exists in the set. Skipping it!"
            )

    def _is_element_id_in(self, element_id):
        return element_id in self._set.keys()

    def get_element(self, element_id: Any) -> Union[DisjointSet.Element, None]:
        if self._is_element_id_in(element_id):
            return self._set[element_id]
        return None

    # TODO: Separate into different types such as path_compression, path_halving, path_splitting
    def find(self, element_id: Any) -> Union[DisjointSet.Element, None]:
        if self._is_element_id_in(element_id):
            element = self._set[element_id]
        else:
            error_print(f"Element id {element_id} does not exist in the set!")
            return None
        if element != element.parent:
            self._set[element.id_].parent = self.find(element.parent.id_)
        return element.parent

    # TODO: Separate into different types such by_rank and by_size
    def union(self, element1_id, element2_id) -> None:
        root_element1 = self.find(element1_id)
        root_element2 = self.find(element2_id)

        if not root_element1 or not root_element2 or root_element1 == root_element2:
            return

        if root_element1.rank > root_element2.rank:
            self._set[root_element1.id_].size += self._set[root_element2.id_].size
            self._set[root_element2.id_].parent = self._set[root_element1.id_]
        elif root_element1.rank < root_element2.rank:
            self._set[root_element2.id_].size += self._set[root_element1.id_].size
            self._set[root_element1.id_].parent = self._set[root_element2.id_]
        else:
            self._set[root_element1.id_].size += self._set[root_element2.id_].size
            self._set[root_element2.id_].parent = self._set[root_element1.id_]
            self._set[root_element1.id_].rank = root_element1.rank + 1
