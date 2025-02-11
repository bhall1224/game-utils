import pygame

from abc import ABC, abstractmethod
from typing import Any, Callable, Literal, Optional, TypedDict

DataCallback = Optional[Callable[[float], float]]


class VectorAction(TypedDict):
    input_id: int
    action_type: Literal["axis", "button"]
    action_name: str
    data_callback: DataCallback


class Controller(ABC):
    @abstractmethod
    def direction(self) -> pygame.Vector2:
        raise NotImplementedError()

    def rotation(self, axis: Literal["x", "y", "z"]) -> pygame.Vector2:
        raise NotImplementedError()

    def action(self, key: str) -> float:
        raise NotImplementedError()


class JoystickController(Controller):
    def __init__(
        self,
        input: pygame.joystick.JoystickType,
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

    def action(self, key: str) -> float:
        vector_action = self._actions.get(key)

        if vector_action is not None:
            id = vector_action["input_id"]
            action_type = vector_action["action_type"]
            if action_type == "axis":
                axis = self.input.get_axis(id)
                print(f"Action {action_type} ID {id} value {axis}")
                vector_callback = vector_action["data_callback"]
                if vector_callback is not None:
                    axis = vector_callback(axis)
                    print(f"controller output {axis}")
                return axis
            else:
                print(f"Button {id}")
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

    def get_keys(self) -> Any:
        return pygame.key.get_pressed()

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


def get_controllers() -> list[pygame.joystick.JoystickType]:
    joysticks = []

    if pygame.joystick.get_count() > 0:
        for j in range(pygame.joystick.get_count()):
            new_joystick = pygame.joystick.Joystick(j)
            joysticks.append(new_joystick)

    return joysticks
