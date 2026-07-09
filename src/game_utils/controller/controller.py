from typing import Any, TypedDict
from enum import IntEnum, auto
from numpy import array
from pygame import joystick
from pygame import event
from pygame import (
    K_RIGHT,
    K_LEFT,
    K_UP,
    K_DOWN,
    K_a,
    K_s,
    K_d,
    K_w,
    K_ESCAPE,
    JOYAXISMOTION,
    JOYBALLMOTION,
    JOYBUTTONDOWN,
    JOYBUTTONUP,
    JOYDEVICEADDED,
    JOYDEVICEREMOVED,
    JOYHATMOTION,
)

#####################################################################################
# Constants and configurations for mapping controller input to action
#####################################################################################

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


#####################################################################################
# Classes for controller behavior and configuration
#####################################################################################

class Controller:
    def __init__(
        self,
        speed: float,
        *args: ControllerMapping,
    ):
        """Creates new instance of Controller object with the given speed scalar and actions

        Args:
            speed (float, optional): Scalar multiple applied to controller output. Defaults to 1.
            *args (VectorAction): A list of action metadata for the controller
            **kwargs (VectorAction): A mapping of metadata for the controller
        """
        self.speed: float = speed
        self.actions: dict[str, ControllerMapping] = {v["input_id"]: v for v in args}

class JoystickController(Controller):
    """Special instance of Controller for handling Joystick (pygame.joystick) input.
    """

    def __init__(
        self,
        input: joystick.JoystickType,
        speed: float,
        *args: ControllerMapping,
    ):
        """_summary_

        Args:
            input (pygame.JoystickType): The pygame Joystick reference
            speed (float, optional): Scalar multiple applied to controller output.
            *args (VectorAction): A list of action metadata for the controller
        """
        super().__init__(speed, *args)
        self.input = input



#####################################################################################
# Methods for annotating event handlers and other methods for contoller registration
#####################################################################################

__CONTROLLERS: dict[str, Controller] = {}

def controller(name=None):
    def __inner(fn):
        # TODO: register controller by instance id
        # should be an event handler type function
        return add_controller(
            name=name or fn.__name__,
            controller=fn
        )
    return __inner

def get_all_controllers():
    return array(__CONTROLLERS.values())

def get_controller(name):
    return __CONTROLLERS.get(name)

def add_controller(name, controller):
    __CONTROLLERS[name] = controller
    return controller

def get_joysticks(
        speed: float,
        *actions: ControllerMapping,
    ):
    """Get a list of joysticks all configured with the same mapping and scalar speed

    Args:
        speed (float): Scalar multiple applied to controller output.

    Raises:
        GameError: Any errors that occur during the game

    Returns:
        JoystickController[]: All connected joysticks as a Py List object
    """        
    return array([
        JoystickController(joystick.Joystick(i), speed, *actions)
        for i in range(joystick.get_count())
    ])


def controller_events(fn):
    def __wrapper(event: event.Event, data: dict[str, Any], **config):
        # TODO: pass event data to controller
        # map controller to instance id
        # grab by instance id per player and pass data
        if event.type == JOYAXISMOTION:
            print("axis movement!")
        elif event.type == JOYHATMOTION:
            print("hat movement!")
        elif event.type == JOYBALLMOTION:
            print("ball movement!")
        elif event.type == JOYBUTTONDOWN:
            print("button down!")
        elif event.type == JOYBUTTONUP:
            print("button up!")
        elif event.type == JOYDEVICEADDED:
            print("JOY ADDED!")
        elif event.type == JOYDEVICEREMOVED:
            print("JOY REMOVED!")
        return fn(event, data, **config)
    return __wrapper
        
#####################################################################################
# Constants and configurations for specific controllers
#####################################################################################

DEFAULT_KEYBOARD_ACTIONS: list[ControllerMapping] = array([
    {
        "input_id": K_RIGHT,
        "action_name": DefaultCommand.X_AXIS_POS.name,
        "action_type": ActionType.BUTTON.value,
    },
    {
        "input_id": K_LEFT,
        "action_name": DefaultCommand.X_AXIS_NEG.name,
        "action_type": ActionType.BUTTON.value,
    },
    {
        "input_id": K_DOWN,
        "action_name": DefaultCommand.Y_AXIS_POS.name,
        "action_type": ActionType.BUTTON.value,
    },
    {
        "input_id": K_UP,
        "action_name": DefaultCommand.Y_AXIS_NEG.name,
        "action_type": ActionType.BUTTON.value,
    },
    {
        "input_id": K_d,
        "action_name": DefaultCommand.X_AXIS_POS.name,
        "action_type": ActionType.BUTTON.value,
    },
    {
        "input_id": K_a,
        "action_name": DefaultCommand.X_AXIS_NEG.name,
        "action_type": ActionType.BUTTON.value,
    },
    {
        "input_id": K_s,
        "action_name": DefaultCommand.Y_AXIS_POS.name,
        "action_type": ActionType.BUTTON.value,
    },
    {
        "input_id": K_w,
        "action_name": DefaultCommand.Y_AXIS_NEG.name,
        "action_type": ActionType.BUTTON.value,
    },
    {
        "input_id": K_ESCAPE,
        "action_name": DefaultCommand.QUIT.name,
        "action_type": ActionType.BUTTON.value,
    },
])

class XBoxAxis(IntEnum):
    LX_AXIS = auto()
    LY_AXIS = auto()
    RX_AXIS = auto()
    RY_AXIS = auto()
    L_TRIGGER = auto()
    R_TRIGGER = auto()


class XBoxButton(IntEnum):
    A_BUTTON = auto()
    B_BUTTON = auto()
    X_BUTTON = auto()
    Y_BUTTON = auto()
    L_BUMPER = auto()
    R_BUMPER = auto()
    BACK_BUTTON = auto()
    START_BUTTON = auto()
    L_STICK_BUTTON = auto()
    R_STICK_BUTTON = auto()
    HOME_BUTTON = auto()


class XBoxHat(IntEnum):
    X = auto()
    Y = auto()