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
                self.width = self.screen.get_width()
                self.height = self.screen.get_height()
            else:
                self.width = width
                self.height = height
                self.screen = pygame.display.set_mode((width, height))

    def __init__(
        self,
        screen_settings: ScreenSettings,
        player_sprite: GameSprite | None = None,
        *other_sprites: GameSprite,
    ):
        """Create new instance of Game object

        Args:
            settings (Settings): Information needed to update the screen
            player_sprite (GameSprite): The sprite to be used for the player
            *other_sprites (GameSprite): Any other sprites needed for the game
        """
        self.dt = 0
        self.running = False
        self.screen_settings = screen_settings
        self.player_sprite = player_sprite
        self.other_sprites = other_sprites
        self.other_sprites_group = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        for sprite in other_sprites:
            self.other_sprites_group.add(sprite)

    def run(self, *event_handlers: Callable[[pygame.event.Event], None]):
        """Runs and maintains the game loop and clock.
        Invokes pygame.quit() when pygame.QUIT event is reached
        """
        self.running = True
        while self.running:
            self.dt = self._get_delta_time()
            self._update_screen()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                for handler in event_handlers:
                    handler(event)
        pygame.quit()

    def _update_sprites(self):
        """Defines behavior for all GameSprite objects over time

        Args:
            dt (float): change in time
        """
        pass

    def _update_collisions(self):
        """Defines behavior for collisions between GameSprite objects over time

        Args:
            dt (float): change in time
        """
        pass

    def _get_delta_time(self) -> float:
        return self.clock.tick(self.screen_settings.frames_per_second) / 1000

    @abstractmethod
    def _update_screen(self):
        raise NotImplementedError
