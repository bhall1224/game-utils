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
        input: pygame.joystick.JoystickType,
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


__NPC_CONTROLLERS: dict[str, Controller] = {}

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
    return [
        JoystickController(pygame.joystick.Joystick(i), speed, *actions)
        for i in range(pygame.joystick.get_count())
    ]

def keyboard_controller(*actions):
    def __inner(fn):
        def __helper(**config):
            speed = config.get("controller", {}).get("speed", 0.0)
            controller = Controller(speed, *actions)
            return fn(controller, **config)
        return __helper
    return __inner

def default_keyboard_controller(*actions):
    return keyboard_controller(*DEFAULT_KEYBOARD_ACTIONS, *actions)

def joystick_controller(player: int = 0, *actions: ControllerMapping):
    """Annotate a configured or non configured method to inject a given JoystickController
    into the player creation function.  

    Args:
        player (int, optional): The player to assign this joystick. Defaults to 0.
        *actions: The list of configured controller actions

    Returns: the annotated method
    """    
    def __inner(fn):
        def __helper(**config):
            speed = config.get("controller", {}).get("speed", 0.0)
            joysticks = get_joysticks(speed, *actions)
            controller = joysticks[player]
            return fn(controller, **config)
        return __helper
    return __inner


def npc_controller(name=None, *actions: ControllerMapping):
    def __inner(fn):
        def __helper(**config):
            speed = config.get("controller", {}).get("speed", 0.0)
            controller = Controller(speed, *actions)
            __NPC_CONTROLLERS[
                name or str(len(__NPC_CONTROLLERS.items()))
            ] = controller
            return fn(controller, **config)
        return __helper
    return __inner

def get_npc_controller(name):
    return __NPC_CONTROLLERS.get(name)

def get_npc_controllers():
    return list(__NPC_CONTROLLERS.values())