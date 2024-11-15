from abc import ABC, abstractmethod
from typing import Optional, Union

from pygame import QUIT, Surface
from pygame.display import flip as flip_display
from pygame.display import set_mode as create_screen
from pygame.event import get as get_game_events
from pygame.time import Clock

from controller import Controller
from sprites import GameSprite


class Game(ABC):
    class Settings:
        def __init__(
            self,
            width: float,
            height: float,
            frames_per_second: int = 60,
            bg_color: Optional[Union[str, tuple[int, int, int]]] = None,
            bg_image: Optional[Surface] = None,
        ):
            self.height = height
            self.width = width
            self.bg_image = bg_image
            self.bg_color = bg_color
            self.frames_per_second = frames_per_second

    def __init__(
        self,
        settings: Settings,
        controllers: list[Controller],
        player_sprite: GameSprite,
        *other_sprites: GameSprite
    ):
        self.settings = settings
        self.controllers = controllers
        self.player_sprite = player_sprite
        self.screen = create_screen((self.settings.width, self.settings.height))
        self.other_sprites = other_sprites

    def run(self):
        clock = Clock()
        dt = 0
        while not self._is_quit():
            self._update_screen()
            self._update_sprites(dt)
            flip_display()
            dt = self._get_delta_time(clock)

    @abstractmethod
    def _update_sprites(self, dt: float):
        raise NotImplementedError

    def _get_delta_time(self, clock: Clock) -> float:
        return clock.tick(self.settings.frames_per_second) / 1000

    def _update_screen(self):
        if self.settings.bg_image is not None:
            self.screen.blit(self.settings.bg_image, (0, 0))
        elif self.settings.bg_color is not None:
            self.screen.fill(self.settings.bg_color)

    def _is_quit(self) -> bool:
        for event in get_game_events():
            if event.type == QUIT:
                return True

        return False
