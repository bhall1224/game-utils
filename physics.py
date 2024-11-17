from loguru import logger
from pygame import Vector2

ZERO_VECTOR = Vector2(0, 0)


class PhysicsBody:
    def __init__(
        self, mass: float = 1.0, position: Vector2 = ZERO_VECTOR, friction: float = 1.0
    ) -> None:
        self.mass = mass
        self.velociy = ZERO_VECTOR
        self.position = position
        self.friction = friction

    def force(self, acceleration: Vector2, d_time: float) -> Vector2:
        force = acceleration * self.mass * self.friction
        self.velociy += force * d_time / self.mass
        self.move(d_time)
        return self.velociy

    def move(self, d_time: float) -> Vector2:
        self.position = move(
            position=self.position,
            velocity=self.velociy,
            dt=d_time,
        )

        return self.position

    def on_collide(self, other):
        assert isinstance(other, PhysicsBody)
        logger.debug(f"received physics body {other}")

    def __str__(self) -> str:
        return str(self.position)


def move(position: Vector2, velocity: Vector2, dt: float) -> Vector2:
    return position + velocity * dt
