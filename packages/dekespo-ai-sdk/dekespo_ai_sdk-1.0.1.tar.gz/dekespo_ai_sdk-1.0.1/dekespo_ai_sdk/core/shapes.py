from abc import ABC, abstractmethod
from enum import Enum, auto

from dekespo_ai_sdk.core.dimensions import Dim2D
from dekespo_ai_sdk.core.assertion import check_positive_value


class Shape2DType(Enum):
    RECTANGLE = auto()
    CIRCLE = auto()
    POINT = auto()


class Shape2D(ABC):
    @abstractmethod
    def __str__(self):
        """ Abstract """

    def __repr__(self):  # pragma: no cover
        return self.__str__()

    @abstractmethod
    def is_inside_boundaries(self, position):
        """ Abstract """

    @abstractmethod
    def get_position(self):
        """ Abstract """


# TODO: Can use classmethod here?
class Rectangle(Shape2D):
    def __init__(self, top_left_corner: Dim2D, width, height):
        self.top_left_corner = top_left_corner
        check_positive_value(width)
        check_positive_value(height)
        self.width = width
        self.height = height

    def __str__(self):
        return (
            f"top_left_corner = {self.top_left_corner}, "
            f"width x height: {self.width}x{self.height}"
        )

    def is_inside_boundaries(self, position):
        if (
            position.x < self.top_left_corner.x
            or position.x >= self.top_left_corner.x + self.width
            or position.y < self.top_left_corner.y
            or position.y >= self.top_left_corner.y + self.height
        ):
            return False
        return True

    def get_four_corner_points(self):
        x, y = self.top_left_corner
        return (
            Dim2D(x, y),
            Dim2D(x + self.width, y),
            Dim2D(x, y + self.height),
            Dim2D(x + self.width, y + self.height),
        )

    def get_position(self):
        return self.top_left_corner


class Circle(Shape2D):
    def __init__(self, centre, radius):
        self.centre = centre
        check_positive_value(radius)
        self.radius = radius

    def __str__(self):
        return f"centre: {self.centre}, radius: {self.radius}"

    def is_inside_boundaries(self, position):
        """ Not filled yet """

    @staticmethod
    def circle_vs_circle_intersection_check(circle1, circle2):
        dist = Dim2D.get_euclid_distance(circle1.centre, circle2.centre)
        total_radius = circle1.radius + circle2.radius
        return dist <= total_radius

    def get_position(self):
        return self.centre


class Point(Shape2D):
    def __init__(self, position):
        self.position = position

    def __str__(self):
        return f"position: {self.position}"

    def is_inside_boundaries(self, position):
        """ Not used """

    def get_position(self):
        return self.position
