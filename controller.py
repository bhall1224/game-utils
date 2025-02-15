from abc import ABC, abstractmethod
from typing import Any, Literal, TypedDict

from pygame import Vector2
from pygame.key import get_pressed as get_pressed_keys
from pygame.joystick import Joystick, JoystickType
from pygame.joystick import get_count as get_joystick_count


class VectorAction(TypedDict):
    input_id: int
    action_type: Literal["axis", "button"]
    action_name: str


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

    def action(self, key: str) -> float:
        vector_action = self._actions.get(key)

        if vector_action is not None:
            id = vector_action["input_id"]
            action_type = vector_action["action_type"]
            if action_type == "axis":
                axis = self.input.get_axis(id)
                print(f"Action {action_type} ID {id} value {axis}")
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
        return get_pressed_keys()

    def action(self, key: str) -> float:
        vector_action = self._actions.get(key)

        if vector_action is not None:
            id = vector_action["input_id"]
            all_keys = self.get_keys()
            if len(all_keys) > 0 and all_keys[id] is True:
                return 1.0

        return 0.0


class ControllerHandler:
    ControllerType = Controller

    @classmethod
    def get_joystick_controller(
        cls, joystick: JoystickType, speed: int
    ) -> ControllerType:
        raise NotImplementedError

    @classmethod
    def get_controllers(
        cls,
        players: int = 1,
        speed: int = 1,
    ) -> list[ControllerType]:
        joysticks = []

        if get_joystick_count() >= players:
            for j in range(players):
                new_joystick = cls.get_joystick_controller(
                    joystick=Joystick(j),
                    speed=speed,
                )
                joysticks.append(new_joystick)

        return joysticks
