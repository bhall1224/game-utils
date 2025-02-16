from abc import abstractmethod
from typing import Optional, Union
import pygame

from .sprites import GameSprite


class Game:
    """Game class defines high-level game logic. This class includes a run method, which controls the game loop.
    User is required to implement abstract methods _update_sprites and optionally _update_collisions.  These methods
    are referenced in run()
    """

    class Settings:
        """Summary class defines information needed to udpate the screen"""

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
        """Create new instance of Game object

        Args:
            settings (Settings): Information needed to update the screen
            player_sprite (GameSprite): The sprite to be used for the player
            *other_sprites (GameSprite): Any other sprites needed for the game
        """
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
        """Runs and maintains the game loop and clock.
        Invokes pygame.quit() when pygame.QUIT event is reached
        """
        clock = pygame.time.Clock()
        dt = 0
        while not self._is_quit():
            self._update_screen()
            self._update_sprites(dt)
            self._update_collisions(dt)
            pygame.display.flip()
            dt = self._get_delta_time(clock)
        pygame.quit()

    @abstractmethod
    def _update_sprites(self, dt: float):
        """Defines behavior for all GameSprite objects over time

        Args:
            dt (float): change in time
        """
        pass

    def _update_collisions(self, dt: float):
        """Defines behavior for collisions between GameSprite objects over time

        Args:
            dt (float): change in time
        """
        pass

    def _get_delta_time(self, clock: pygame.time.Clock) -> float:
        return clock.tick(self.settings.frames_per_second) / 1000

    def _update_screen(self):
        """Blits the screen if there's a background image and fills background color, if they exist in the settings"""
        if self.settings.bg_image is not None:
            self.screen.blit(self.settings.bg_image, (0, 0))
        if self.settings.bg_color is not None:
            self.screen.fill(self.settings.bg_color)

    def _is_quit(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        return False
