from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Literal, TypedDict

from pygame import Vector2
from pygame.key import get_pressed as get_pressed_keys
from pygame.joystick import Joystick, JoystickType
from pygame.joystick import get_count as get_joystick_count
from pygame.locals import *


class VectorAction(TypedDict):
    input_id: int
    action_type: Literal["axis", "button"]
    action_name: str


class Controller(ABC):
    def __init__(
        self,
        speed: int = 1,
        *args: VectorAction,
        **kwargs: VectorAction,
    ):
        self.speed = speed

        self._actions: dict[str, VectorAction] = {}
        for action in args:
            id = action["action_name"]
            self._actions[id] = action
        self._actions.update(kwargs)

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
    ):
        super().__init__(speed, *args, **kwargs)
        self.input = input

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
    class Commands(Enum):
        X_AXIS_POS = "x_axis_pos"
        X_AXIS_NEG = "x_axis_neg"
        Y_AXIS_POS = "y_axis_pos"
        Y_AXIS_NEG = "y_axis_neg"

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


class DefaultKeyboardController(KeyboardController):
    def direction(self) -> Vector2:
        vx = (
            self.action(self.Commands.X_AXIS_POS.value)
            - self.action(self.Commands.X_AXIS_NEG.value)
        ) * self.speed

        vy = (
            self.action(self.Commands.Y_AXIS_POS.value)
            - self.action(self.Commands.Y_AXIS_NEG.value)
        ) * self.speed

        return Vector2(vx, vy)


DEFAULT_KEYBOARD_CONTROLLER = DefaultKeyboardController(
    1500,
    {
        "input_id": K_RIGHT,
        "action_name": KeyboardController.Commands.X_AXIS_POS.value,
        "action_type": "button",
    },
    {
        "input_id": K_LEFT,
        "action_name": KeyboardController.Commands.X_AXIS_NEG.value,
        "action_type": "button",
    },
    {
        "input_id": K_DOWN,
        "action_name": KeyboardController.Commands.Y_AXIS_POS.value,
        "action_type": "button",
    },
    {
        "input_id": K_UP,
        "action_name": KeyboardController.Commands.Y_AXIS_NEG.value,
        "action_type": "button",
    },
)


class ControllerHandler:
    ControllerType = Controller

    @classmethod
    def new_controller_instance(
        cls,
        joystick: JoystickType,
        speed: int,
        *args: VectorAction,
        **kwargs: VectorAction,
    ) -> ControllerType:
        raise NotImplementedError

    @classmethod
    def get_controllers(
        cls,
        players: int = 1,
        speed: int = 1,
    ) -> list[ControllerType]:
        joysticks = []
        print(f"controller type: {cls.ControllerType.__name__}")
        if get_joystick_count() >= players:
            for j in range(players):
                new_joystick = cls.new_controller_instance(
                    joystick=Joystick(j),
                    speed=speed,
                )
                joysticks.append(new_joystick)

        return joysticks
