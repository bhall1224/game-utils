from loguru import logger
from numpy.random import normal
from pygame import Vector2

ZERO_VECTOR = Vector2(0, 0)


class PhysicsBody:
    GRAVITY = 9.8

    def __init__(
        self,
        mass: float = 1.0,
        position: Vector2 = ZERO_VECTOR,
        friction: float = 0.0,
        elasticity: float = 1.0,
        slip: float = 1.0,
    ) -> None:
        self.mass = mass
        self.velociy = ZERO_VECTOR
        self.position = position
        self.friction = friction
        self.k_friction = 0
        self.elasticity = elasticity
        self.slip = slip

    def force(self, acceleration: Vector2, dtime: float) -> Vector2:
        force = acceleration * dtime

        if (
            self.k_friction == 0
            and abs(force.magnitude()) > self.normal_force() * self.friction
        ) or (abs(force.magnitude()) > self.normal_force() * self.k_friction):
            if self.friction > 0 and self.k_friction == 0:
                self.k_friction = self.friction * normal(loc=self.slip)
            self.velociy += force
            self.move(dtime)

        return self.velociy

    def move(self, dtime: float) -> Vector2:
        self.position = move(
            position=self.position,
            velocity=self.velociy,
            dt=dtime,
        )

        return self.position

    def on_collide(self, other):
        # New velocity is given by V`= (V(m-s) + U2s)/(m+s)
        # for initial magnitudes Vm(self) and Us(other)
        assert isinstance(other, PhysicsBody)

        logger.trace(f"received physics body {other}")
        logger.trace(f"my velocity: {self.velociy}")
        self.velociy *= self.mass - other.mass
        self.velociy += other.velociy * 2 * other.mass
        self.velociy /= self.mass + other.mass

        # energy loss, if any
        self.velociy *= self.elasticity

    def momentum(self) -> Vector2:
        return self.velociy * self.mass

    def normal_force(self) -> float:
        return self.mass * self.GRAVITY

    def __str__(self) -> str:
        return str(self.position)


def move(position: Vector2, velocity: Vector2, dt: float) -> Vector2:
    return position + velocity * dt
