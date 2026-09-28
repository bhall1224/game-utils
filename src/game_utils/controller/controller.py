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
# Class for controller behavior and configuration
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
# Class for assigning and registering controllers
#####################################################################################

class Controllers:
    def __init__(self):
        self.__controllers = {}

    def add(self, name):
        def __inner(fn):
            self.__controllers[name] = fn()
            return fn
        return __inner

    def controller(self, joy_id):
        def __inner(fn):
            def __sprite_fn_wrapper(config):
                return fn(self.__controllers[joy_id], config)
            return __sprite_fn_wrapper
        return __inner

    def controllers(self):
        def __inner(fn):
            def __sprite_fn_wrapper(config):
                return fn(self.__controllers, config)
            return __sprite_fn_wrapper
        return __inner

