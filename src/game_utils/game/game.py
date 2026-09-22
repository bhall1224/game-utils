from typing import Any
import os
import pygame
import json


from game_utils import sprites
from game_utils.clock import get_delta_time
from game_utils.controller.controller import Controller
from game_utils.screen.screen import ScreenSettings
from game_utils.sprites.sprites import GameSprite

# module relies heavily on pygame
# initializing at module import insures
# everything is ready
if not pygame.get_init():
    print("pygame not initialized, initializing now...")
    pygame.init()

# A special user event for changing scenes within the event listener
NEXT_SCENE_EVENT = pygame.USEREVENT

# Constant defaults for screen refresh
FRAMERATE = 60.0
UNITS = 1000.0  # pygame clock returns ms - take s as default


class ScreenRefresh:
    framerate = FRAMERATE
    units = UNITS


class Scene:
    def __init__(
        self,
        screen,
        player: sprites.GameSprite,
        other_sprites: list[sprites.GameSprite] = [],
        config: dict[str, Any] = {},
        screen_refresh=ScreenRefresh(),
    ):
        self.__screen = screen
        self.__player = player
        self.__other_sprites = other_sprites.copy()
        self.__config = config.copy()
        self.__screen_refresh = screen_refresh

    def update_screen(self):
        self.__screen.update_screen()

    def update_player(self, new_pos):
        self.__player.update(new_pos)

    def update_other_sprites(self, *sprite_positions):
        map(
            lambda sprite, position: sprite.update(position),
            self.__other_sprites,
            sprite_positions,
        )

    def config(self):
        return self.__config

    def get_delta_time(self):
        return get_delta_time(
            self.__screen_refresh.framerate, self.__screen_refresh.units
        )


class Game:
    def __init__(self):
        self.__config: dict[str, Any] = {}
        self.__scene_mapping: dict[str, Scene] = {}
        self.__sprite_mapping: dict[str, GameSprite] = {}
        self.__screen_settings: dict[str, ScreenSettings] = {}
        self.__controllers: dict[str, Controller]
        self.__current_scene: int = -1

    def run(self, start_scene: str | None = None):
        def __wrapper(run_fn):
            running = True
            scene = self.__get_next_scene(start_scene)
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == NEXT_SCENE_EVENT:
                        next_scene_name = (
                            event.dict.get("scene_name")
                            if event.dict is not None
                            else None
                        )
                        scene = self.__get_next_scene(next_scene_name)
                    else:
                        running = run_fn(scene, event, **self.__config)

            return run_fn

        return __wrapper

    def scene(self, name):
        """Decorate a method to register it as a scene.  A scene is basically an update
        function that will be called once per game loop.  You may register as many as you wish.
        These are inteded for game logic that relies on the change in time, and serve as an entry
        point to your logic.

        Args:
            name (str, optional): Pass an optional name for the scene, which will be added as a tag.
        Defaults to None.
        """

        def __inner(scene_fn):
            # inner method simply registers the function in the map
            self.__scene_mapping[name] = scene_fn()

        return __inner

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

    def inject_config(self, key: str | None = None):
        def __inner(fn):
            def __wrapper(*args, **more_config):
                registered_config = (
                    self.__config.get(key, self.__config) if key else self.__config
                )
                registered_config.update(more_config)
                return fn(*args, **registered_config)

            return __wrapper

        return __inner

    def sprite(self, name: str | None = None):
        def __inner(sprite_fn):
            def __wrapper(**config):
                sprite: GameSprite = sprite_fn(**config)
                self.__sprite_mapping[name] = sprite
                return sprite

            return __wrapper

        return __inner

    def inject_sprites(self):
        def __inner(fn):
            def __wrapper(*args, **config):

                return fn(list(self.__sprite_mapping.values()), *args, **config)

            return __wrapper

        return __inner

    def screen_settings(self, name: str | None = None):
        def __inner(fn):
            self.__screen_settings[name or fn.__name__] = fn()
            return fn

        return __inner

    def inject_screen_settings(self, key: str | None = None):
        def __inner(fn):
            def __wrapper(*args, **config):
                settings = (
                    self.__screen_settings.get(key, ScreenSettings())
                    if key
                    else ScreenSettings
                )
                return fn(settings, *args, **config)

            return __wrapper

        return __inner

    def controller(self, name: str | None = None):
        def __inner(fn):
            self.__controllers[name or fn.__name__] = fn()
            return fn

        return __inner

    def inject_controller(self, key: str | None = None):
            def __inner(fn):
                def __wrapper(*args, **config):
                    controller = (
                        self.__controllers.get(key, Controller())
                        if key
                        else Controller
                    )
                    return fn(controller, *args, **config)
    
                return __wrapper
    
            return __inner

    def __get_next_scene(self, scene_name: str | None = None):
        if scene_name is None:
            self.__current_scene += 1
            return list(self.__scene_mapping.values())[self.__current_scene]
        else:
            return self.__scene_mapping[scene_name]
