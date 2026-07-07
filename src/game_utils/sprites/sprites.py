from typing import Any

from pygame import Rect, Surface, Vector2
from pygame.sprite import Sprite, Group

PLAYER = "player"
__SPRITES = {}
__SPRITE_GROUPS = {}

class GameSprite(Sprite):
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
        self.image = image
        _, _, *dimensions = image.get_rect()
        self.rect = Rect(position.x, position.y, *dimensions)
        self.position = position
        self.boundaries = boundaries

class PhysicsSprite(GameSprite):
    """GameSprite that uses a PhysicsBody reference with which to apply physics"""

    def __init__(
        self,
        image: Surface,
        position: Vector2,
        physics_body: Any,
        boundaries: Rect | None = None,
    ):
        super().__init__(image, position, boundaries)
        self.physics_body = physics_body


class PlayerSprite(PhysicsSprite):
    """GameSprite with PhysicsBody and Controller input"""

    def __init__(
        self,
        image: Surface,
        position: Vector2,
        controller: Any,
        physics_body: Any,
        boundaries: Rect | None = None,
    ):
        super().__init__(image, position, physics_body, boundaries)
        self.controller = controller


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

def sprite_group(name=None):
    def __inner(fn):
        new_sprites = fn()
        __SPRITE_GROUPS[name or fn.__name__] = Group(*new_sprites)
        __SPRITES.update({new_sprites})
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
