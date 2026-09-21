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
# Constants for conventional joystick mappings
#####################################################################################
class XBox:
    XBOX_BUTTONS: list[str] = []
    XBOX_AXES = list[str] = []
    XBOX_HATS = list[str] = []


class Playstation:
    PLAYSTATION_BUTTONS: list[str] = []
    PLAYSTATION_AXES = list[str] = []
    PLAYSTATION_HATS = list[str] = []


class NintendoSwitch:
    NINTEDO_SWITCH_BUTTONS: list[str] = []
    NINTEDO_SWITCH_AXES = list[str] = []
    NINTEDO_SWITCH_HATS = list[str] = []


class NintendoWii:
    NINTEDO_WII_BUTTONS: list[str] = []
    NINTEDO_WII_AXES = list[str] = []
    NINTEDO_WII_HATS = list[str] = []


class NintendoGameCube:
    NINTEDO_GAMECUBE_BUTTONS: list[str] = []
    NINTEDO_GAMECUBE_AXES = list[str] = []
    NINTEDO_GAMECUBE_HATS = list[str] = []


class Nintendo64:
    NINTEDO_64_BUTTONS: list[str] = []
    NINTEDO_64_AXES = list[str] = []
    NINTEDO_64_HATS = list[str] = []


class SuperNintendo:
    SUPER_NINTEDO_BUTTONS: list[str] = []
    SUPER_NINTEDO_AXES = list[str] = []
    SUPER_NINTEDO_HATS = list[str] = []


class NintendoEntertainmentSystem:
    NINTEDO_ES_BUTTONS: list[str] = []
    NINTEDO_ES_AXES = list[str] = []
    NINTEDO_ES_HATS = list[str] = []


class SegaDreamcast:
    SEGA_DREAMCAST_BUTTONS: list[str] = []
    SEGA_DREAMCAST_AXES = list[str] = []
    SEGA_DREAMCAST_HATS = list[str] = []


class SegaGenesis:
    SEGA_DREAMCAST_BUTTONS: list[str] = []
    SEGA_DREAMCAST_AXES = list[str] = []
    SEGA_DREAMCAST_HATS = list[str] = []


class ATARI_2600:
    ATARI_BUTTONS: list[str] = []
    ATARI_AXES = list[str] = []
    ATARI_HATS = list[str] = []


#####################################################################################
# Classes for controller behavior and configuration
#####################################################################################


class Controller:
    def __init__(
        self,
        actions: ControllerActions
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
