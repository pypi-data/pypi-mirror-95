from enum import Enum, auto
from dataclasses import dataclass
from typing import Callable, Iterator, Tuple

from dekespo_ai_sdk.core.dimensions import Dim2D


class NeighbourType(Enum):
    NONE = auto()
    CROSS = auto()
    DIAMOND = auto()
    SQUARE = auto()
    CONNECTIVITY_FOUR = auto()
    CONNECTIVITY_EIGHT = auto()


@dataclass
class NeighbourData:
    type_: NeighbourType = NeighbourType.NONE
    radius: int = 1
    random_output: bool = False
    should_reach: bool = False
    should_block: bool = True


# TODO: Use a custom typing instead?
GetNeighbourFunctionType = Callable[
    [Dim2D, Callable[[Dim2D, bool, bool], bool], NeighbourData],
    Iterator[Tuple[Dim2D, float]],
]


class Neighbour:
    @staticmethod
    def get_neighbours_square(
        position: Dim2D,
        is_position_valid_function: Callable[[Dim2D, bool, bool], bool],
        neighbour_data: NeighbourData = NeighbourData(),
    ) -> Iterator[Tuple[Dim2D, float]]:
        x, y = position.x, position.y
        for y_distance in range(-neighbour_data.radius, neighbour_data.radius + 1):
            for x_distance in range(-neighbour_data.radius, neighbour_data.radius + 1):
                new_position = Dim2D(x + x_distance, y + y_distance)
                is_not_self_position = not (x_distance == 0 and y_distance == 0)
                is_valid_position = is_position_valid_function(
                    new_position,
                    neighbour_data.should_block,
                    neighbour_data.should_reach,
                )
                if is_not_self_position and is_valid_position:
                    yield new_position, abs(x_distance) + abs(y_distance)

    @staticmethod
    def get_neighbours_diamond(
        position: Dim2D,
        is_position_valid_function: Callable[[Dim2D, bool, bool], bool],
        neighbour_data: NeighbourData = NeighbourData(),
    ) -> Iterator[Tuple[Dim2D, float]]:
        x, y = position.x, position.y
        for y_distance in range(-neighbour_data.radius, neighbour_data.radius + 1):
            for x_distance in range(-neighbour_data.radius, neighbour_data.radius + 1):
                new_position = Dim2D(x + x_distance, y + y_distance)
                is_not_self_position = not (x_distance == 0 and y_distance == 0)
                is_valid_position = is_position_valid_function(
                    new_position,
                    neighbour_data.should_block,
                    neighbour_data.should_reach,
                )
                is_within_radius = (
                    abs(x_distance) + abs(y_distance) <= neighbour_data.radius
                )
                if is_not_self_position and is_within_radius and is_valid_position:
                    yield new_position, abs(x_distance) + abs(y_distance)

    @staticmethod
    def get_neighbours_cross(
        position: Dim2D,
        is_position_valid_function: Callable[[Dim2D, bool, bool], bool],
        neighbour_data: NeighbourData = NeighbourData(),
    ) -> Iterator[Tuple[Dim2D, float]]:
        x, y = position.x, position.y
        for distance in range(1, neighbour_data.radius + 1):
            for new_position in (
                Dim2D(x + distance, y),
                Dim2D(x - distance, y),
                Dim2D(x, y + distance),
                Dim2D(x, y - distance),
            ):
                is_valid_position = is_position_valid_function(
                    new_position,
                    neighbour_data.should_block,
                    neighbour_data.should_reach,
                )
                if is_valid_position:
                    yield new_position, distance

    @staticmethod
    def get_neighbour_function_8_connectivity(
        position: Dim2D,
        is_position_valid_function: Callable[[Dim2D, bool, bool], bool],
        neighbour_data: NeighbourData = NeighbourData(),
    ) -> Iterator[Tuple[Dim2D, float]]:
        x, y = position.x, position.y
        for new_position in (
            Dim2D(x - 1, y),
            Dim2D(x - 1, y - 1),
            Dim2D(x, y - 1),
            Dim2D(x + 1, y - 1),
        ):
            is_valid_position = is_position_valid_function(
                new_position,
                neighbour_data.should_block,
                neighbour_data.should_reach,
            )
            if is_valid_position:
                yield new_position, -1

    @staticmethod
    def get_neighbour_function_4_connectivity(
        position: Dim2D,
        is_position_valid_function: Callable[[Dim2D, bool, bool], bool],
        neighbour_data: NeighbourData = NeighbourData(),
    ) -> Iterator[Tuple[Dim2D, float]]:
        x, y = position.x, position.y
        for new_position in (Dim2D(x - 1, y), Dim2D(x, y - 1)):
            is_valid_position = is_position_valid_function(
                new_position,
                neighbour_data.should_block,
                neighbour_data.should_reach,
            )
            if is_valid_position:
                yield new_position, -1
