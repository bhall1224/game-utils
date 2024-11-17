from typing import Any

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

    def force(self, acceleration: Vector2, dtime: float) -> Vector2:
        force = acceleration * self.mass * self.friction
        self.velociy += force * dtime / self.mass
        self.move(dtime)
        return self.velociy

    def move(self, dtime: float) -> Vector2:
        self.position = move(
            position=self.position,
            velocity=self.velociy,
            dt=dtime,
        )

        return self.position

    def on_collide(self, other, dtime: float, loss: Vector2 = ZERO_VECTOR):
        # TODO: this is where collisions happen, and it's broken lol
        assert isinstance(other, PhysicsBody)

        logger.trace(f"received physics body {other}")
        logger.trace(f"my velocity: {self.velociy}")
        acc = (other.velociy * other.mass - self.velociy * self.mass) / dtime
        acc -= loss / dtime
        self.force(acc, dtime)

    def __str__(self) -> str:
        return str(self.position)


def move(position: Vector2, velocity: Vector2, dt: float) -> Vector2:
    return position + velocity * dt
