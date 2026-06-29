from typing import Any

from pygame import Rect, Surface, Vector2
from pygame.sprite import Sprite

PLAYER = "player"
__SPRITES = {}

class GameSprite(Sprite):
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
    """GameSprite that uses a PhysicsBody reference to apply physics"""

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
        sprite_name = name or str(len(__SPRITES.items()))
        __SPRITES[sprite_name] = fn()
        return fn
    return __inner

def sprite_group(fn):
    __SPRITES.update(fn())
    return fn

def player_sprite(name=None):
    def __inner(fn):
        __SPRITES[name or PLAYER] = fn()
        return fn
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
