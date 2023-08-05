from dataclasses import dataclass
from enum import Enum, auto

from dekespo_ai_sdk.core.dimensions import Dim2D
from dekespo_ai_sdk.core.graph import Graph
from dekespo_ai_sdk.core.disjoint_set import DisjointSet
from dekespo_ai_sdk.core.neighbour import NeighbourData, NeighbourType


class ConnectivityType(Enum):
    FOUR = auto()
    EIGHT = auto()


class ConnectedComponentLabelling:
    """
    Works in only binary format data
    """

    @dataclass
    class _Node:
        position: Dim2D
        graph_binary_value: bool
        label_value: int = 0

    def __init__(self, graph: Graph, connectivity_neighbour_type: NeighbourType):
        self.graph = graph
        self.connectivity_neighbour_type = connectivity_neighbour_type
        self._nodes = None
        self._set_nodes()
        self._labels_disjoint_set = DisjointSet()

    def _set_nodes(self):
        self._nodes = {}
        for y, row in enumerate(self.graph.raw_data_handler.raw_data):
            for x, graph_value in enumerate(row):
                self._nodes[Dim2D(x, y)] = ConnectedComponentLabelling._Node(
                    Dim2D(x, y), graph_value not in self.graph.blocking_values
                )

    # TODO: Should return a graph?
    def get_labels_graph(self):
        new_grid = []
        for y, row in enumerate(self.graph.raw_data_handler.raw_data):
            row_list = []
            for x, _ in enumerate(row):
                row_list.append(self._nodes[Dim2D(x, y)].label_value)
            new_grid.append(row_list)
        return new_grid

    def first_pass(self):
        def is_already_labelled(node):
            return node.label_value > 0

        current_label = 0
        for current_node in self._nodes.values():
            if current_node.graph_binary_value:
                new_labels = []
                for neighbour_position, _ in self.graph.get_available_neighbours(
                    current_node.position,
                    NeighbourData(
                        self.connectivity_neighbour_type,
                        should_block=False,
                        should_reach=True,
                    ),
                ).items():
                    neighbour_node = self._nodes[neighbour_position]
                    if is_already_labelled(neighbour_node):
                        new_labels.append(neighbour_node.label_value)

                if not new_labels:
                    current_label += 1
                    current_node.label_value = current_label
                    self._labels_disjoint_set.make_set(
                        DisjointSet.Element(current_label)
                    )
                else:
                    minimum_label = min(new_labels)
                    current_node.label_value = minimum_label
                    for label in new_labels:
                        self._labels_disjoint_set.union(label, minimum_label)

    def second_pass(self):
        for current_node in self._nodes.values():
            if current_node.graph_binary_value:
                current_node.label_value = self._labels_disjoint_set.find(
                    current_node.label_value
                ).id_

    def get_regions(self):
        regions = {}
        for current_node in self._nodes.values():
            try:
                regions[current_node.label_value].append(current_node.position)
            except KeyError:
                regions[current_node.label_value] = [current_node.position]
        return regions
