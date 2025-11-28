import logging
from abc import abstractmethod

import pygame

from .screen import ScreenSettings
from .sprites import GameSprite

logger = logging.getLogger(__name__)


class Game:
    """Game class defines high-level game logic. This class includes a run method, which controls the game loop.
    User is required to implement abstract methods self._update() and self._events(), which is invoked within self.run()
    """

    def __init__(self, screen_settings: ScreenSettings | None = None):
        """Invokes pygame.init(), configures clock and screen settings

        Args:
            screen_settings (ScreenSettings): Any screen settings
        """
        pygame.init()
        self.dt = 0
        self.running = False
        self.screen_settings = screen_settings

    def run(self):
        """Runs and maintains the game loop and clock. Updates the screen and invokes any handlers
        Invokes pygame.quit() when pygame.QUIT event is reached
        """
        logger.debug("starting game...")
        self.running = True
        while self.running:
            self._update()
            if self.screen_settings is not None:
                self.screen_settings.update_screen()
                self.dt = self.screen_settings.get_delta_time()
                pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self._events(event)

        pygame.quit()

    def _events(self, event: pygame.event.Event, *args, **kwargs):
        """Define custom event handlers.  Optional.  Called once per game loop

        Args:
            event (pygame.event.Event): The event passed from run() method
            *args/**kwargs
        """
        pass

    @abstractmethod
    def _update(self):
        """Required implentation of game logic. Called once per game loop.

        Raises:
            NotImplementedError: Required implementation
        """
        raise NotImplementedError()


class SpriteGame(Game):
    def __init__(
        self,
        screen_settings: ScreenSettings,
        player_sprite: GameSprite | None = None,
        *other_sprites: GameSprite,
    ):
        """Create new instance of SpriteGame object.  Invokes pygame.init().  Must
        implement _update_sprites()

        Args:
            settings (ScreenSettings): Information needed to update the screen
            player_sprite (GameSprite): The sprite to be used for the player
            *other_sprites (GameSprite): Any other sprites needed for the game
        """
        super().__init__(screen_settings=screen_settings)
        self.player_sprite = player_sprite
        self.other_sprites = other_sprites
        self.other_sprites_group = pygame.sprite.Group()
        for sprite in other_sprites:
            self.other_sprites_group.add(sprite)

    @abstractmethod
    def _update_sprites(self):
        """Defines behavior for all GameSprite objects over time.  Called once per game loop

        Args:
            dt (float): change in time
        """
        raise NotImplementedError
