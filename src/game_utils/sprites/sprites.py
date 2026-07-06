from typing import Any

from pygame import Rect, Surface, Vector2
from pygame.sprite import Sprite

PLAYER = "player"
__SPRITES = {}

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
        id: int = 0,
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
        self.id = id

class PhysicsSprite(GameSprite):
    """GameSprite that uses a PhysicsBody reference with which to apply physics"""

    def __init__(
        self,
        image: Surface,
        position: Vector2,
        physics_body: Any,
        boundaries: Rect | None = None,
        id: int = 0,
    ):
        super().__init__(image, position, boundaries, id)
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
        id: int = 0,
    ):
        super().__init__(image, position, physics_body, boundaries, id)
        self.controller = controller


def sprite(name=None):
    def __inner(fn):
        sprite: GameSprite = fn()
        sprite_name: str = name or fn.__name__
        __SPRITES[sprite_name] = sprite
        return fn
    return __inner

def sprite_group(fn):
    __SPRITES.update(fn())
    return fn

def player_sprite(name=None):
    def __inner(fn):
        return sprite(name)(fn)
    return __inner

def update_sprites(fn):
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
