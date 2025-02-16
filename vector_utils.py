from numpy.random import choice, rand
from pygame import Vector2


def get_random_vector(scalar_mag: int = 1, non_negative: bool = False) -> Vector2:
    def rand_sign() -> int:
        return choice([-1, 1]) if not non_negative else 1

    return Vector2(
        x=rand() * rand_sign() * scalar_mag,
        y=rand() * rand_sign() * scalar_mag,
    )


def bounce_y(v: Vector2) -> Vector2:
    """Changes direction of a vector with respect to Y axis"""
    v.y *= -1

    return v


def bounce_x(v: Vector2) -> Vector2:
    """Changes direction of a vector with respect to X axis"""
    v.x *= -1
    return v


def zero_y(v: Vector2) -> Vector2:
    """Stops movement in the Y direction"""
    v.y = 0
    return v


def zero_x(v: Vector2) -> Vector2:
    """Stops movement in the X direction"""
    v.x = 0
    return v


def torus_y(v: Vector2, bounds: Vector2) -> Vector2:
    """Repositions Y assuming the surface world is a Torus shape

    Args:
        v (Vector2): Position vector
        bounds (Vector2): (Y min, Y max)

    Returns:
        Vector2: Updated position
    """
    y_min = bounds.x
    y_max = bounds.y
    if v.y > y_max:
        v.y = y_min
    elif v.y < y_min:
        v.y = y_max

    return v


def torus_x(v: Vector2, bounds: Vector2) -> Vector2:
    """Repositions X assuming the surface world is a Torus shape

    Args:
        v (Vector2): Position vector
        bounds (Vector2): (X min, X max)

    Returns:
        Vector2: Updated position
    """
    x_min = bounds.x
    x_max = bounds.y
    if v.x > x_max:
        v.x = x_min
    elif v.x < x_min:
        v.x = x_max

    return v
