from __future__ import annotations
import math
from typing import Iterator, List, Tuple, Union


class Dim2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"(x: {self.x}, y: {self.y})"

    def __repr__(self) -> str:  # pragma: no cover
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Dim2D):
            raise TypeError("The other must be Dim2D but found", type(other))
        return self.x == other.x and self.y == other.y

    def __add__(self, other: Dim2D) -> Dim2D:
        return Dim2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Dim2D) -> Dim2D:
        return Dim2D(self.x - other.x, self.y - other.y)

    def vectoral_multiply(self, other: Dim2D) -> Dim2D:
        return Dim2D(self.x * other.x, self.y * other.y)

    def constant_multiply(self, value: float) -> Dim2D:
        return Dim2D(self.x * value, self.y * value)

    def vectoral_divide(self, other: Dim2D) -> Dim2D:
        return Dim2D(self.x / other.x, self.y / other.y)

    def constant_divide(self, value: float):
        return Dim2D(self.x / value, self.y / value)

    def round(self):
        self.x = round(self.x)
        self.y = round(self.y)

    def __abs__(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @staticmethod
    def convert_candiates_to_dimensions(
        candidates: Union[List, Tuple],
    ) -> Iterator[Dim2D]:
        for x, y in candidates:
            yield Dim2D(x, y)

    @staticmethod
    def get_average_value(dimensions):
        total_dimensions_values = Dim2D(0, 0)
        if not dimensions:
            return total_dimensions_values
        for dimension in dimensions:
            total_dimensions_values += dimension
        return total_dimensions_values.constant_divide(len(dimensions))

    @staticmethod
    def get_euclid_distance(point1, point2):
        return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

    @staticmethod
    def get_manathan_distance(point1, point2):
        return abs(point1.x - point2.x) + abs(point1.y - point2.y)

    @staticmethod
    def get_minimum_index_and_value(dimensions, criteria_function, **kwargs):
        def minimum_operator(value, minimum):
            return value < minimum

        return Dim2D._get_optimum_index_and_value(
            dimensions, criteria_function, minimum_operator, **kwargs
        )

    @staticmethod
    def get_maximum_index_and_value(dimensions, criteria_function, **kwargs):
        def maximum_operator(value, maximum):
            return value > maximum

        return Dim2D._get_optimum_index_and_value(
            dimensions, criteria_function, maximum_operator, **kwargs
        )

    @staticmethod
    def _get_optimum_index_and_value(
        dimensions, criteria_function, operator_function, **kwargs
    ):
        start_index = 0
        optimum_dimension = dimensions[start_index]
        optimum_value = criteria_function(dimensions[start_index], **kwargs)
        for dimension in dimensions:
            new_value = criteria_function(dimension, **kwargs)
            if operator_function(new_value, optimum_value):
                optimum_dimension = dimension
                optimum_value = new_value
        return optimum_dimension, optimum_value

    def __hash__(self):
        return hash((self.x, self.y))

    def __iter__(self):
        return iter((self.x, self.y))


class Dim3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"x: {self.x}, y: {self.y}, z: {self.z}"

    def __repr__(self):  # pragma: no cover
        return self.__str__()
