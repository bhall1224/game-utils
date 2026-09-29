from collections.abc import Callable
from typing import Any, Concatenate
import os
import pygame
import json

from game_utils.screen import ScreenSettings

#####################################################################################
# Class for registering screen settings and configurations
#####################################################################################


class Game:
    def __init__(self):
        self.__screen_settings = ScreenSettings()
        self.__config: dict[str, Any] = {}
        self.__running = False
        self.__event_handler: Callable[
            [pygame.event.Event, ScreenSettings, dict[str, Any]], bool
        ]

    def event_handler(self, event_func):
        self.__event_handler = event_func
        return event_func

    def run(self, screen=True):
        if not pygame.get_init():
            pygame.init()

        self.__running = True

        if screen:
            self.__screen_settings.activate()

        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                else:
                    self.__running = self.__event_handler(
                        event, self.__screen_settings, self.__config
                    )

    def config(self, fn):
        self.__config = fn()
        return fn

    def inject_config(self, fn):
        def __wrapper():
            return fn(self.__config)

        return __wrapper

    def screen_settings(self, fn):
        self.__screen_settings = fn(self.__config)
        return fn
    
    def inject_screen_settings(self, fn):
        """Also injects config

        Args:
            fn (function): The function in which to inject config and screen settings
        """

        def __wrapper():
            return fn(self.__screen_settings, self.__config)

        return __wrapper

    def quit(self, cleanup_callbacks=[]):
        """Any cleanup logic.  Calls pygame.quit()

        Args:
            cleanup_callbacks (list, optional): List of any () -> None callbacks for extra cleanup logic. Defaults to [].
        """
        for cleanup_callback in cleanup_callbacks:
            cleanup_callback()

        pygame.quit()
