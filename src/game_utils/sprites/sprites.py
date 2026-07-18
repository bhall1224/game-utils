from collections.abc import Callable
from enum import Enum
from typing import Any

from pygame import Rect, Surface, Vector2
from pygame.sprite import Sprite, Group

from game_utils.game import GameError

__SPRITES = {}

class GameSprite(Sprite):
    CONTROLLER_INPUT = "controller"
    DELTA_TIME = "dt"

    """_summary_

    Args:
        id (int): unique id for the sprite.  can be ordinal
        image (pygame.Surface): Surface on which to draw the sprite
        position (pygame.Vector2): Position on screen to draw the sprite
        boundaries (pygame.Rect | None): Optional boundaries in which to keep the sprite.  Defaults to None
    """
    def __init__(
        self,
        image: Surface,
        position: Vector2,
        boundaries: Rect | None = None,
    ):
        """Implement a Game Sprite object. Subclass must implement GameSprite.update

        Args:
            image (Surface): The image for the sprite
            position (Vector2): Where to put the sprite
            boundaries (Rect | None, optional): Optional boundary coordinates
        """
        super().__init__()
        self._image = image
        self._position = position
        self._boundaries = boundaries

    def update(self, *args, **kwargs):
        """update this sprite with given information

        Args:
            dt (float): the change in time
            controller_input (Vector2): the vector with which to update this sprite's position
        """
        if len(args) > 0 and isinstance(args[0], float):
            dt = args[0]
        elif self.DELTA_TIME in kwargs.keys():
            dt = kwargs[self.DELTA_TIME]
        else:
            raise GameError("no argument for delta time given")
        
        if len(args) > 1 and isinstance(args[1], Callable[[float, Vector2], Vector2]):
            controller_input = args[1]
        elif self.CONTROLLER_INPUT in kwargs.keys():
            controller_input = kwargs[self.CONTROLLER_INPUT]
        else:
            raise GameError("no callback for controller input given")

        self._image = controller_input(dt, self._position)

    def get_rect(self):
        return self._image.get_rect()
    
    def get_position(self):
        return self._position
    
    def set_position(self, position: Vector2):
        self._position = position

    def boundary_behavior(
        self,
        along_x_axis: Callable[[Vector2], Vector2],
        along_y_axis: Callable[[Vector2], Vector2]
    ):
        if self._boundaries is None:
            return
        
        if self._position.x > self._boundaries.width or self._position < self._boundaries.left:
            self._position = along_x_axis(self._position)

        if self._position.y > self._boundaries.height or self._position < self._boundaries.top:
            self._position = along_y_axis(self._position)


def sprite(name=None):
    """Annotate a function that returns a GameSprite.  
    If a name is provided, use that as the key; otherwise, the function's name is used.

    Args:
        name (str, optional): A unique name for the sprite. Defaults to None.
    """
    def __inner(fn):
        # Store the sprite in the global __SPRITES dictionary
        __SPRITES[
            name or fn.__name__
        ] = fn()
        return fn
    return __inner

def player_sprite(name=None):
    def __inner(fn):
        return sprite(name)(fn)
    return __inner

def inject_sprites(fn):
    def __inner(dt, **config):
        return fn(dt, __SPRITES, **config)
    return __inner

def sprite_boundaries(name=None):
    def __inner(fn):
        if name is not None:
            sprite_ = __SPRITES.get(name)
            if sprite_ is not None and sprite_.boundaries is not None:
                sprite_.position = fn(sprite_)
            else:
                for sprite_ in __SPRITES.values():
                    sprite_.position = fn(sprite_)
        return fn
    return __inner
