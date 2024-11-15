from abc import ABC, abstractmethod
from typing import Callable, Optional

from pygame import Vector2

VectorAction = Callable[[], float]
# ButtonAction = Callable[[bool],]


class Controller(ABC):
    def __init__(
        self,
        speed: float,
        x_axis: VectorAction,
        y_axis: VectorAction,
        dpad_x: Optional[VectorAction] = None,
        dpad_y: Optional[VectorAction] = None,
        axes: Optional[list[VectorAction]] = None,
        actions: Optional[list[VectorAction]] = None,
    ) -> None:
        self.speed = speed
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.dpad_x = dpad_x
        self.dpad_y = dpad_y
        self.axes = axes
        self.actions = actions

    @abstractmethod
    def direction(self, position: Vector2, time: float) -> Vector2:
        raise NotImplementedError()

    def rotation(
        self, position: Vector2, axis: float, time: float, speed: float = 1.0
    ) -> Vector2:
        raise NotImplementedError()

    def commands(self, keys_pressed: dict[str, bool]) -> None:
        raise NotImplementedError()
