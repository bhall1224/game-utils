from abc import abstractmethod
from typing import Any, Optional
from loguru import logger
from pygame import Rect, Surface, Vector2
from pygame.sprite import Sprite

from .controller import Controller
from .physics import PhysicsBody


class GameSprite(Sprite):
    def __init__(
        self,
        image: Surface,
        position: Vector2,
        boundaries: Optional[Rect] = None,
        id: int = 0,
    ):
        """Implement a Game Sprite object. Subclass must GameSprite.update

        Args:
            image (Surface): The image for the sprite
            position (Vector2): Where to put the sprite
            boundaries (Optional[Rect], optional): Optional boundary vectors for this sprite (xmax, xmin, ymax, ymin). Defaults to None.
        """
        super().__init__()
        self.image = image
        _, _, *dimensions = image.get_rect()
        self.rect = Rect(position.x, position.y, *dimensions)
        self.position = position
        self.boundaries = boundaries
        self.id = id

    @abstractmethod
    def update(self, *args: Any, **kwargs: Any):
        pass

    def _update_pos(self, *args: Any, **kwargs: Any):
        """Updates position of this sprite.  If I have boundaries,
        I will bind this sprite's position.
        Pass callables in **kwargs.

        Args:
            xbounds (() -> None): a function to call when X bounds is met
            ybounds (() -> None): a function to call when Y bounds is met
        """
        xbounds = kwargs.get("xbounds")
        ybounds = kwargs.get("ybounds")
        x, y, w, h = self.rect

        if self.boundaries is not None:
            bx_max, bx_min, by_max, by_min = self.boundaries

            if self.position.y > by_max - h / 2:
                if ybounds is not None:
                    ybounds()

                self.position.y = by_max - h / 2

            elif self.position.y < by_min + h / 2:
                if ybounds is not None:
                    ybounds()

                self.position.y = by_min + h / 2

            if self.position.x > bx_max - w / 2:
                if xbounds is not None:
                    xbounds()

                self.position.x = bx_max - w / 2

            elif self.position.x < bx_min + w / 2:
                if xbounds is not None:
                    xbounds()

                self.position.x = bx_min + w / 2

        x = self.position.x - w / 2
        y = self.position.y - h / 2

        self.rect = Rect(x, y, w, h)

    def __str__(self) -> str:
        return str(tuple(self.rect))


class PhysicsSprite(GameSprite):
    def __init__(
        self,
        image: Surface,
        position: Vector2,
        physics_body: PhysicsBody,
        boundaries: Optional[Rect] = None,
        id: int = 0,
    ):
        super().__init__(image, position, boundaries, id)
        self.physics_body = physics_body
        self.physics_body.position = self.position


class PlayerSprite(PhysicsSprite):
    def __init__(
        self,
        image: Surface,
        position: Vector2,
        controller: Controller,
        physics_body: PhysicsBody,
        boundaries: Optional[Rect] = None,
        id: int = 0,
    ):
        super().__init__(image, position, physics_body, boundaries, id)
        self.controller = controller
