from typing import Any
import os
import pygame
import json
import inspect


# module relies heavily on pygame
# initializing at module import insures
# everything is ready
if not pygame.get_init():
    print("pygame not initialized, initializing now...")
    pygame.init()


class Game:
    def __init__(self):
        self.__config: dict[str, Any] = {}
        self.__running = True

    def run(self, event_func):           
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                else:
                    self.__running = event_func(event, **self.__config)

        return event_func

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
        fn_info = inspect.signature(fn)
        params = list(fn_info.parameters.values())
        return lambda *params: fn(*params, **self.__config)
