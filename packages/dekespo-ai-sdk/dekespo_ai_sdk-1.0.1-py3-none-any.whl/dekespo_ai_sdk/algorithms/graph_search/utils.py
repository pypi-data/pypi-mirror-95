from collections import OrderedDict
from dataclasses import dataclass
from typing import Callable, List

from dekespo_ai_sdk.core.dimensions import Dim2D
from dekespo_ai_sdk.core.neighbour import NeighbourData


@dataclass
class SearchData:
    start_point: Dim2D
    # bug in mypy: https://github.com/python/mypy/issues/5485
    get_available_neighbours: Callable[[Dim2D, NeighbourData], OrderedDict]  # type: ignore
    neighbour_data: NeighbourData


@dataclass(frozen=True)
class Node:
    position: Dim2D
    distance: int

    def __eq__(self, other):
        if not isinstance(other, Node):
            raise TypeError(f"Mismatch type with {type(other)}")

        return self.position == other.position


def update_sets(
    closed_set: List[Node],
    open_set: List[Node],
    current_node: Node,
    input_data: SearchData,
):
    if current_node not in closed_set:
        closed_set.append(current_node)
        for (  # type: ignore
            new_candidate_point,  # type: ignore
            new_distance,  # type: ignore
        ) in input_data.get_available_neighbours(  # type: ignore
            current_node.position, input_data.neighbour_data  # type: ignore
        ).items():
            open_set.append(
                Node(new_candidate_point, current_node.distance + new_distance)
            )
