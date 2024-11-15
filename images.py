from typing import Optional

from loguru import logger
from pygame import Rect, Surface


class SpriteSheet:
    def __init__(self, spritesheet: Surface, bg_color: Optional[str] = None) -> None:
        self.spritesheet = spritesheet
        self.rect = self.spritesheet.get_rect()
        self.bg_color = bg_color

    def get(self, rect: Rect) -> Surface:
        logger.trace(rect)
        image = Surface(rect.size)
        if self.bg_color is not None:
            image.fill(self.bg_color)
        image.blit(self.spritesheet, (0, 0), rect)
        return image
