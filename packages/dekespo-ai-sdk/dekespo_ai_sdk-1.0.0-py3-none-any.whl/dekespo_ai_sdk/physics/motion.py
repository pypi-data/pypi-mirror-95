from dekespo_ai_sdk.core.dimensions import Dim2D
from dekespo_ai_sdk.core.assertion import check_positive_value
from dekespo_ai_sdk.core.shapes import Shape2D


class Motion2D:
    @property
    def position(self):
        return self._position

    @property
    def velocity(self):
        return self._velocity

    @property
    def acceleration(self):
        return self._acceleration

    @property
    def momentum(self):
        return self._momentum

    @property
    def mass(self):
        return self._mass

    def __init__(
        self, shape: Shape2D, velocity=Dim2D(0, 0), acceleration=Dim2D(0, 0), mass=None
    ):
        self.shape = shape
        self._position = shape.get_position()
        self._velocity = velocity
        self._acceleration = acceleration
        self._jerk = Dim2D(0, 0)
        if mass is not None:
            check_positive_value(mass)
        self._mass = mass
        self._momentum = self._calculate_momentum()

    def __str__(self):
        string = f"Position: {self.position}"
        string += f"\nVelocity: {self.velocity}"
        string += f"\nAcceleration: {self.acceleration}"
        string += f"\nMass: {self.mass}"
        string += f"\nMomentum: {self.momentum}"
        return string

    def __repr__(self):  # pragma: no cover
        return self.__str__()

    def _calculate_momentum(self):
        if self.mass:
            return self.velocity.constant_multiply(self.mass)
        return None

    def apply_force(self, force):
        # pylint: disable=attribute-defined-outside-init
        if self.mass:
            self._jerk = force.constant_divide(self.mass)

    def update(self):
        def update_position():
            self._position += self._jerk.constant_multiply(1 / 6)
            self._position += self._acceleration.constant_multiply(0.5)
            self._position += self._velocity

        def update_velocity():
            self._velocity += self._jerk.constant_multiply(0.5)
            self._velocity += self._acceleration

        def update_momentum():
            self._momentum = self._calculate_momentum()

        def update_acceleration():
            self._acceleration += self._jerk
            self._jerk = Dim2D(0, 0)

        update_position()
        update_velocity()
        update_momentum()
        update_acceleration()
