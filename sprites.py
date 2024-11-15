from abc import ABC, abstractmethod
from typing import Any, Optional

from pygame import Rect, Surface, Vector2
from pygame.sprite import Sprite


class GameSprite(Sprite, ABC):
    def __init__(
        self,
        image: Surface,
        position: Vector2,
        boundaries: Optional[Rect] = None,
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

    @abstractmethod
    def update(self, *args: Vector2, **kwargs: Any):
        pass

    def __str__(self) -> str:
        return str(tuple(self.rect))
