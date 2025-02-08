from abc import ABC, abstractmethod
from typing import Any, Callable, Literal, Optional, TypedDict, Union
from loguru import logger
from pygame import Vector2
from pygame.joystick import JoystickType
from pygame.key import get_pressed

DataCallback = Optional[Callable[[float], float]]


class VectorAction(TypedDict):
    input_id: int
    action_type: Literal["axis", "button"]
    action_name: str
    data_callback: DataCallback


class Controller(ABC):
    @abstractmethod
    def direction(self) -> Vector2:
        raise NotImplementedError()

    def rotation(self, axis: Literal["x", "y", "z"]) -> Vector2:
        raise NotImplementedError()

    def action(self, key: str) -> float:
        raise NotImplementedError()


class JoystickController(Controller):
    def __init__(
        self,
        input: JoystickType,
        speed: int = 1,
        *args: VectorAction,
        **kwargs: VectorAction,
    ) -> None:
        self.input = input
        self.speed = speed

        self._actions: dict[str, VectorAction] = {}
        for action in args:
            id = action["action_name"]
            self._actions[id] = action
        self._actions.update(kwargs)
        logger.trace(f"joystick actions: {self._actions}")

    def action(self, key: str) -> float:
        vector_action = self._actions.get(key)

        if vector_action is not None:
            id = vector_action["input_id"]
            action_type = vector_action["action_type"]
            if action_type == "axis":
                axis = self.input.get_axis(id)
                vector_callback = vector_action["data_callback"]
                if vector_callback is not None:
                    axis = vector_callback(axis)
                return axis
            else:
                return 1.0 if self.input.get_button(id) else 0.0

        else:
            return 0.0


class KeyboardController(Controller):
    def __init__(
        self,
        speed: int = 1,
        *args: VectorAction,
        **kwargs: VectorAction,
    ) -> None:
        self.speed = speed
        self._actions: dict[str, VectorAction] = {}
        for action in args:
            id = action["action_name"]
            self._actions[id] = action
        self._actions.update(kwargs)
        logger.trace(f"keyboard actions: {self._actions}")

    def get_keys(self) -> Any:
        return get_pressed()

    def action(self, key: str) -> float:
        vector_action = self._actions.get(key)

        if vector_action is not None:
            id = vector_action["input_id"]
            data_callback = vector_action["data_callback"]
            all_keys = self.get_keys()
            if len(all_keys) > 0 and all_keys[id] is True:
                if data_callback is not None:
                    return data_callback(1)

        return 0.0
