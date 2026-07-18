import pygame
from typing import TypedDict
from enum import IntEnum, auto

class DefaultCommand(IntEnum):
    """Default controller configurations"""
    X_AXIS_POS = auto()
    X_AXIS_NEG = auto()
    Y_AXIS_POS = auto()
    Y_AXIS_NEG = auto()
    QUIT = auto()
    ACTION_1 = auto()
    ACTION_2 = auto()

class ActionType(IntEnum):
    BUTTON = auto()
    AXIS = auto()
    HAT = auto()

class ControllerMapping(TypedDict):
    input_id: int
    action_type: int
    action_name: str

DEFAULT_KEYBOARD_ACTIONS: list[ControllerMapping] = [
    {
        "input_id": pygame.K_RIGHT,
        "action_name": DefaultCommand.X_AXIS_POS.name,
        "action_type": ActionType.BUTTON.value,
    },
    {
        "input_id": pygame.K_LEFT,
        "action_name": DefaultCommand.X_AXIS_NEG.name,
        "action_type": ActionType.BUTTON.value,
    },
    {
        "input_id": pygame.K_DOWN,
        "action_name": DefaultCommand.Y_AXIS_POS.name,
        "action_type": ActionType.BUTTON.value,
    },
    {
        "input_id": pygame.K_UP,
        "action_name": DefaultCommand.Y_AXIS_NEG.name,
        "action_type": ActionType.BUTTON.value,
    },
    {
        "input_id": pygame.K_d,
        "action_name": DefaultCommand.X_AXIS_POS.name,
        "action_type": ActionType.BUTTON.value,
    },
    {
        "input_id": pygame.K_a,
        "action_name": DefaultCommand.X_AXIS_NEG.name,
        "action_type": ActionType.BUTTON.value,
    },
    {
        "input_id": pygame.K_s,
        "action_name": DefaultCommand.Y_AXIS_POS.name,
        "action_type": ActionType.BUTTON.value,
    },
    {
        "input_id": pygame.K_w,
        "action_name": DefaultCommand.Y_AXIS_NEG.name,
        "action_type": ActionType.BUTTON.value,
    },
    {
        "input_id": pygame.K_ESCAPE,
        "action_name": DefaultCommand.QUIT.name,
        "action_type": ActionType.BUTTON.value,
    },
]
