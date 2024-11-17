from abc import ABC, abstractmethod
from typing import Any, Callable, Literal, Optional, TypedDict

from loguru import logger
from pygame import Vector2
from pygame.joystick import JoystickType

DataCallback = Optional[Callable[[Optional[Any]], None]]


class Data(TypedDict):
    name: str


class VectorAction(TypedDict):
    joystick_id: int
    data: Data


class JoystickConfig(ABC):
    def __init__(
        self,
        joystick: JoystickType,
        speed: int = 1,
        *args: VectorAction,
        **kwargs: VectorAction
    ) -> None:
        self.joystick = joystick
        self.speed = speed

        self._axes: dict[str, int] = {}
        for arg in args:
            name = arg["data"]["name"]
            self._axes[name] = arg["joystick_id"]

        self._buttons = kwargs

    @abstractmethod
    def x_axis(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def y_axis(self) -> float:
        raise NotImplementedError

    def dpad_x(self) -> Literal[-1, 0, 1]:
        return 0

    def dpad_y(self) -> Literal[-1, 0, 1]:
        return 0

    def axes(self, name: str) -> float:
        axis = self._axes.get(name)

        if axis is not None:
            return self.joystick.get_axis(axis)

        return 0.0

    def actions(self, name: str, data_callback: Optional[DataCallback] = None) -> bool:
        button = self._buttons.get(name)
        if button is not None:
            if data_callback is not None:
                data_callback(button["data"])
            return self.joystick.get_button(button["joystick_id"])

        return False


class Controller(ABC):
    def __init__(self, joystick_config: JoystickConfig) -> None:
        self.joystick_config = joystick_config

    @abstractmethod
    def direction(self) -> Vector2:
        raise NotImplementedError()

    def rotation(self, axis: Literal["x", "y", "z"]) -> Vector2:
        raise NotImplementedError()

    def button_commands(self, button: str) -> bool:
        return self.joystick_config.actions(button)

    def axis_commands(self, name: str) -> float:
        return self.joystick_config.axes(name)
