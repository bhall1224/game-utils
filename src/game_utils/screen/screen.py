
from typing import Any

import pygame.display as display
from pygame import FULLSCREEN, Color, Surface

ColorType = str | tuple[int, int, int] | Color

class ScreenSettings:
    def __init__ (
        self,
        width: float = 0.0,
        height: float = 0.0,
        title: str | None = None,
        bg_color: ColorType | None = None,
        bg_image: Surface | None = None,
        display_mod: Any = display
    ):
        self.display_mod = display_mod
        if width == 0.0 and height == 0.0:
            self.screen_surface = self.display_mod.set_mode((0, 0), FULLSCREEN)
            self.width = self.screen_surface.get_width()
            self.height = self.screen_surface.get_height()
        else:
            self.screen_surface = self.display_mod.set_mode((width, height))
            self.width = width
            self.height = height

        if title is not None:
            self.display_mod.set_caption(title)
        
        self.bg_color = bg_color
        self.bg_image = bg_image
        
__SETTINGS_MAPPING: dict[str, ScreenSettings] = {}

def screen_settings(name=None):
    def __inner(fn):
        __SETTINGS_MAPPING[name or fn.__name__] = fn()
        return fn
    return __inner

def screen_update(name=None):
    def __inner(fn):
        def __inner_callback(data, **config):
            settings = __SETTINGS_MAPPING[name or fn.__name__]
            if settings.bg_color is not None:
                settings.screen_surface.fill(settings.bg_color)
            elif settings.bg_image is not None:
                settings.screen_surface.blit(settings.bg_image, (settings.width, settings.height))
            settings.display_mod.flip()
            return fn(data, settings, **config)
        return __inner_callback        
    return __inner
