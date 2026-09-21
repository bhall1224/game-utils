from collections.abc import Callable
from pygame import Vector2, joystick, key, locals

from game_utils.physics.physics import PhysicsBody

if not joystick.get_init():
    joystick.init()

ButtonAction = Callable[[None], bool]
AxisAction = Callable[[None], float]
HatAction = Callable[[None], Vector2]

class KeyboardController:
    def __init__(self, default_actions: dict[int, ButtonAction]):
        self.__actions = default_actions

    def action(self, key: int):
        return self.__actions[key]()


class Controller:
    def __init__(
        self,
        buttons: list[ButtonAction] = [],
        axes: list[AxisAction] = [],
        hats: list[HatAction] = [],
    ):
        self.__buttons = buttons
        self.__axes = axes
        self.__hats = hats

    def button(self, index):
        return self.__buttons[index]()

    def axis(self, index):
        return self.__axes[index]()

    def hat(self, index):
        return self.__hats[index]()
    
def inject_controller(sprite, buttons: list[ButtonAction] = [], axes: list[AxisAction] = [], hats: list[HatAction] = []):
    """Injects a controller into a sprite object.  This will create a new Controller
    object and assign it to the sprite's controller attribute.

    Args:
        sprite (GameSprite): The sprite to inject the controller into
        buttons (list[ButtonAction]): The list of button actions
        axes (list[AxisAction]): The list of axis actions
        hats (list[HatAction]): The list of hat actions
    """
    if not hasattr(sprite, "controller"):
        raise AttributeError("Sprite does not have a controller attribute")

    sprite.controller = Controller(
        buttons=buttons,
        axes=axes,
        hats=hats
    )

        
# key.K_RIGHT: {
#         "action_name": DefaultCommand.X_AXIS_POS.name,
#         "action_type": ActionType.BUTTON.value,
#     },
#      pygame.K_LEFT:{
#         "action_name": DefaultCommand.X_AXIS_NEG.name,
#         "action_type": ActionType.BUTTON.value,
#     },
#     pygame.K_DOWN: {
#         "action_name": DefaultCommand.Y_AXIS_POS.name,
#         "action_type": ActionType.BUTTON.value,
#     },
#     pygame.K_UP: {
#         "action_name": DefaultCommand.Y_AXIS_NEG.name,
#         "action_type": ActionType.BUTTON.value,
#     },
#     pygame.K_d: {
#         "action_name": DefaultCommand.X_AXIS_POS.name,
#         "action_type": ActionType.BUTTON.value,
#     },
#     pygame.K_a: {
#         "action_name": DefaultCommand.X_AXIS_NEG.name,
#         "action_type": ActionType.BUTTON.value,
#     },
#     pygame.K_s: {
#         "action_name": DefaultCommand.Y_AXIS_POS.name,
#         "action_type": ActionType.BUTTON.value,
#     },
#     pygame.K_w: {
#         "action_name": DefaultCommand.Y_AXIS_NEG.name,
#         "action_type": ActionType.BUTTON.value,
#     },
#     pygame.K_ESCAPE: {
#         "action_name": DefaultCommand.QUIT.name,
#         "action_type": ActionType.BUTTON.value,
#     },