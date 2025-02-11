from abc import ABC, abstractmethod
from typing import Optional, Union
import pygame

from .sprites import GameSprite


class Game(ABC):
    class Settings:
        def __init__(
            self,
            width: float,
            height: float,
            frames_per_second: int = 60,
            bg_color: Optional[Union[str, tuple[int, int, int]]] = None,
            bg_image: Optional[pygame.Surface] = None,
        ):
            self.height = height
            self.width = width
            self.bg_image = bg_image
            self.bg_color = bg_color
            self.frames_per_second = frames_per_second

    def __init__(
        self, settings: Settings, player_sprite: GameSprite, *other_sprites: GameSprite
    ):
        self.settings = settings
        self.player_sprite = player_sprite
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height)
        )
        self.other_sprites = other_sprites
        self.other_sprites_group: pygame.sprite.Group = pygame.sprite.Group()
        for sprite in other_sprites:
            self.other_sprites_group.add(sprite)

    def run(self):
        clock = pygame.time.Clock()
        dt = 0
        while not self._is_quit():
            self._update_screen()
            self._update_sprites(dt)
            self._update_collisions(dt)
            pygame.display.flip()
            dt = self._get_delta_time(clock)
        quit()

    @abstractmethod
    def _update_sprites(self, dt: float):
        """how do you want to update the sprites at each turn

        Args:
            dt (float): change in time
        """
        pass

    def _update_collisions(self, dt: float):
        """how do you want to update sprites upon collision

        Args:
            dt (float): change in time
        """
        pass

    def _get_delta_time(self, clock: pygame.time.Clock) -> float:
        return clock.tick(self.settings.frames_per_second) / 1000

    def _update_screen(self):
        if self.settings.bg_image is not None:
            self.screen.blit(self.settings.bg_image, (0, 0))
        elif self.settings.bg_color is not None:
            self.screen.fill(self.settings.bg_color)

    def _is_quit(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        return False
