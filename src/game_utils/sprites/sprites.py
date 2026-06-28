from typing import Any

from pygame import Rect, Surface, Vector2
from pygame.sprite import Sprite

__PLAYER = "player"
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
            boundaries (Rect | None, optional): Optional boundary vectors for this sprite (xmax, xmin, ymax, ymin). Defaults to None.
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
        self.physics_body.position = self.position


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

def sprites(fn):
    __SPRITES.update(fn())
    return fn

def player_sprite(fn):
    __SPRITES[__PLAYER] = fn()
    return fn

def update_sprites(fn):
    def __inner(dt, **config):
        return fn(dt, __SPRITES, **config)
    return __inner