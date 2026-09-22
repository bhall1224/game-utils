from collections.abc import Callable
from pygame import Vector2, joystick
from game_utils.math import is_probably

if not joystick.get_init():
    joystick.init()

#####################################################################################
# Type aliases for callback function types
#####################################################################################

ButtonAction = Callable[[None], bool]
AxisAction = Callable[[float], float]
HatAction = Callable[[Vector2], Vector2]


class ControllerActions:
    def __init__(
        self,
        button_actions: list[ButtonAction] = [],
        axis_actions: list[AxisAction] = [],
        hat_actions: list[HatAction] = [],
    ):
        self.buttons = button_actions
        self.axes = axis_actions
        self.hats = hat_actions



#####################################################################################
# Classes for controller behavior and configuration
#####################################################################################


class Controller:
    def __init__(
        self,
        actions: ControllerActions = ControllerActions()
    ):
        self.__buttons = actions.buttons
        self.__axes = actions.axes
        self.__hats = actions.hats

    def button(self, index):
        return self.__buttons[index]()

    def axis(self, index):
        return self.__axes[index]()

    def hat(self, index):
        return self.__hats[index]()



#####################################################################################
# functions for injecting controllers into sprites
#####################################################################################


def add_controller_to_sprite(sprite, actions: ControllerActions):
    """Injects a controller into a sprite object.  This will create a new Controller
    object and assign it to the sprite's controller attribute.

    Args:
        sprite (GameSprite): The sprite to inject the controller into
        buttons (list[ButtonAction]): The list of button actions
        axes (list[AxisAction]): The list of axis actions
        hats (list[HatAction]): The list of hat actions
    """
    sprite.controller = Controller(
        buttons=actions.buttons, axes=actions.axes, hats=actions.hats
    )


#####################################################################################
# Annotation methods for direct injection
#####################################################################################
__REGISTERED_CONTROLLER_ACTIONS: dict[str, ControllerActions] = {}


def button_action(id: str, action_name: str):
    def __inner(fn):
        __REGISTERED_CONTROLLER_ACTIONS.get(id, ControllerActions()).buttons[
            action_name
        ] = fn
        return fn()

    return __inner


def axis_action(id: str, action_name: str):
    def __inner(fn):
        __REGISTERED_CONTROLLER_ACTIONS.get(id, ControllerActions()).axes[
            action_name
        ] = fn
        return fn()

    return __inner


def hat_action(id: str, action_name: str):
    def __inner(fn):
        __REGISTERED_CONTROLLER_ACTIONS.get(id, ControllerActions()).hats[
            action_name
        ] = fn
        return fn()

    return __inner


def inject_controller(id: str):
    """annotate a method that returns a sprite, and this will inject the sprite with a given
    physics body configuration

    Args:
        fn (function): the method to annotate
    """

    def __wrapper(fn):
        sprite_ = fn()
        add_controller_to_sprite(
            sprite=sprite_,
            actions=__REGISTERED_CONTROLLER_ACTIONS.get(id, ControllerActions()),
        )
        return fn()

    return __wrapper


#####################################################################################
# Summoning all joysticks and realtime joystick handling
#####################################################################################


def assign_joysticks():
    for i in range(joystick.get_count()):
        new_joystick = joystick.Joystick(i)
