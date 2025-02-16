from numpy.random import normal
from pygame import Vector2, Vector3


class PhysicsBody:
    """Applies physics to a GameSprite"""

    ZERO_VECTOR = Vector2(0, 0)
    GRAVITY = 9.8

    def __init__(
        self,
        mass: float = 1.0,
        position: Vector2 = ZERO_VECTOR.copy(),
        friction: float = 0.0,
        elasticity: float = 1.0,
        slip: float = 1.0,
    ) -> None:
        self.mass = mass
        self.velociy = self.ZERO_VECTOR.copy()
        self.position = position
        self.static_friction = friction
        self.kinetic_friction = 0
        self.elasticity = elasticity
        if self.static_friction > 0:
            self.kinetic_friction = self.static_friction * normal(loc=slip)

    def force(self, acceleration: Vector2, dtime: float) -> Vector2:
        new_velocity = acceleration * dtime
        force = acceleration * self.mass

        if force.magnitude() > self.friction_force().magnitude():
            self.velociy += new_velocity
        else:
            self.velociy -= self.velociy * self.friction_force().magnitude() * dtime
        self.move(dtime)

        return self.velociy

    def move(self, dtime: float) -> Vector2:
        self.position += self.velociy * dtime

        return self.position

    def on_collide(self, other):
        # New velocity is given by V`= (V(m-s) + U2s)/(m+s)
        # for initial magnitudes Vm(self) and Us(other)
        assert isinstance(other, PhysicsBody)

        self.velociy *= self.mass - other.mass
        self.velociy += other.velociy * 2 * other.mass
        self.velociy /= self.mass + other.mass

        # energy loss, if any
        self.velociy *= self.elasticity

    def momentum(self) -> Vector2:
        return self.velociy * self.mass

    def normal_force(self) -> Vector3:
        return Vector3(0, 0, self.mass * self.GRAVITY)

    def friction_force(self) -> Vector3:
        return (
            self.static_friction * self.normal_force()
            if self.velociy == self.ZERO_VECTOR
            else self.kinetic_friction * self.normal_force()
        )

    def __str__(self) -> str:
        return str(self.position)
