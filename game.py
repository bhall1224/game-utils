from abc import abstractmethod
from collections.abc import Callable
import pygame

from .sprites import GameSprite


class Game:
    """Game class defines high-level game logic. This class includes a run method, which controls the game loop.
    User is required to implement abstract methods _update_sprites and optionally _update_collisions.  These methods
    are referenced in run()
    """

    class ScreenSettings:
        """defines information needed to udpate the screen"""

        def __init__(
            self,
            width: float = 0.0,
            height: float = 0.0,
            frames_per_second: int = 60,
            bg_color: tuple[int, int, int] | str | None = None,
            bg_image: pygame.Surface | None = None,
        ):
            self.bg_image = bg_image
            self.bg_color = bg_color
            self.frames_per_second = frames_per_second
            if width == 0.0 and height == 0.0:
                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            self.width = self.screen.get_width()
            self.height = self.screen.get_height()

    def __init__(
        self,
        screen_settings: ScreenSettings,
        player_sprite: GameSprite,
        *other_sprites: GameSprite,
    ):
        """Create new instance of Game object

        Args:
            settings (Settings): Information needed to update the screen
            player_sprite (GameSprite): The sprite to be used for the player
            *other_sprites (GameSprite): Any other sprites needed for the game
        """
        self.running = False
        self.screen_settings = screen_settings
        self.player_sprite = player_sprite
        self.other_sprites = other_sprites
        self.other_sprites_group: pygame.sprite.Group = pygame.sprite.Group()
        for sprite in other_sprites:
            self.other_sprites_group.add(sprite)

    def run(self, *event_handlers: Callable[[pygame.event.Event], None]):
        """Runs and maintains the game loop and clock.
        Invokes pygame.quit() when pygame.QUIT event is reached
        """
        self.running = True
        clock = pygame.time.Clock()
        dt = 0
        while self.running:
            self._update_screen()
            self._update_sprites(dt)
            self._update_collisions(dt)
            dt = self._get_delta_time(clock)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                for handler in event_handlers:
                    handler(event)
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
        return clock.tick(self.screen_settings.frames_per_second) / 1000

    def _update_screen(self):
        """Blits the screen if there's a background image and fills background color, if they exist in the settings"""
        if self.screen_settings.bg_image is not None:
            self.screen_settings.screen.blit(self.screen_settings.bg_image, (0, 0))
        if self.screen_settings.bg_color is not None:
            self.screen_settings.screen.fill(self.screen_settings.bg_color)
