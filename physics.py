from loguru import logger
from pygame import Vector2


def move(
    position: Vector2, velocity: Vector2, dt: float, scale: float = 1.0
) -> Vector2:
    logger.trace(f"velocity for movement: {velocity}")
    return position + velocity * scale * dt
