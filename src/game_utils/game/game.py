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
        self.__event_handler: Callable[[pygame.event.Event, ScreenSettings, dict[str, Any]], bool]

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
                    self.__running = self.__event_handler(event, self.__screen_settings, self.__config)

    def config(
        self,
        config_path: str | None = None,
        config_file: str | None = None,
        assets_path: str | None = None,
        resources_path: str | None = None,
    ):
        """Register a configuration handler () -> Any
        This function will be called once at the start of the game


        Args:
            config_path (str | None, optional): Path to the configuration file. Defaults to None.
            config_file (str | None, optional): Name of the configuration file. Defaults to None.
            assets_path (str | None, optional): Path to the assets directory. Defaults to None.
            resources_path (str | None, optional): Path to the resources directory. Defaults to None

        Returns:
            () -> Any: A special callback function for handling configuration data.
        """

        def __inner(fn):
            def __config_path(path, file):
                return os.path.join(os.getcwd(), path, file)

            def __wrapper():
                config = fn() or {}
                config_file_path = __config_path(
                    config_path or ".config", config_file or "config.json"
                )
                if os.path.exists(config_file_path):
                    with open(config_file_path, "r") as f:
                        config.update(json.load(f))

                assets_file_path = assets_path or ".assets"

                if os.path.exists(assets_file_path):
                    config["ASSETS_PATH"] = assets_file_path
                    os.environ["ASSETS_PATH"] = assets_file_path

                resources_file_path = resources_path or ".resources"
                if os.path.exists(resources_file_path):
                    config["RESOURCES_PATH"] = resources_file_path
                    os.environ["RESOURCES_PATH"] = resources_file_path

                self.__config.update(config)

                return config

            return __wrapper

        return __inner

    def inject_config(self, fn):
        def __wrapper():
            return fn(self.__config)
        return __wrapper

    def screen_settings(self):
        def __inner(fn):
            self.__screen_settings = fn(self.__config)
            return fn
        return __inner

    def inject_screen_settings(self, fn):
        """Also injects config

        Args:
            fn (function): The function in which to inject config and screen settings
        """
        def __wrapper():
            return fn(self.__screen_settings, self.__config)
        return __wrapper
