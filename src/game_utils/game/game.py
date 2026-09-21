from typing import Any
import os
import pygame
import json

from game_utils import sprites, get_delta_time

# module relies heavily on pygame
# initializing at module import insures
# everything is ready
if not pygame.get_init():
    print("pygame not initialized, initializing now...")
    pygame.init()

# A special user event for changing scenes within the event listener
NEXT_UPDATE_EVENT = pygame.USEREVENT

# Constant defaults for screen refresh
FRAMERATE = 60.0
UNITS = 1000.0 # pygame clock returns ms - take s as default

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
            screen_refresh = ScreenRefresh(),
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
        return get_delta_time(self.__screen_refresh.framerate, self.__screen_refresh.units)
    

# global reference in memory for registered scenes
__SCENE_MAPPING: dict[str, Scene] = {}

# global reference in memory for configuration dictionary
__CONFIGURATION: dict[str, Any] = {}

__SPRITE_MAPPING: dict[str, sprites.GameSprite]

# __CONTROLLER_MAPPING: dict[str, Controller]


def run(event_handler_fn):
    running = True

    while running:
        scene = __scenes_as_list()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == NEXT_UPDATE_EVENT:
                if event.dict is not None:
                    __SCENE_MAPPING.update(event.dict)
                __SCENE_MAPPING.pop(scene.__name__)
            else:
                running = event_handler_fn(event, scene, **__CONFIGURATION)

    return event_handler_fn


def scene(name):
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
        __SCENE_MAPPING[name] = scene_fn()

    return __inner


def register_config(
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

            __CONFIGURATION.update(config)

            return config

        return __wrapper
    return __inner

def config(key=None):
    def __inner(fn):
        def __wrapper(*args, **_):
            registered_config = __CONFIGURATION.get(key, __CONFIGURATION) if key else __CONFIGURATION
            return fn(*args, **registered_config)
        return __wrapper
    return __inner

def register_sprite(name):
    def __inner(sprite_fn):
        def __wrapper(**config):
            sprite = sprite_fn(**config)
            __SPRITE_MAPPING[name] = sprite
            return sprite
        return __wrapper
    return __inner

def sprite(name):
    def __inner(fn):
        def __wrapper(sprite, *args, **config):
            sprite = __SPRITE_MAPPING[name]
            return fn(sprite, *args, **config)
        return __wrapper
    return __inner

# def register_controller(id):

def tag(*args, **kwargs):
    """Set attributes to functions with which you can search using search methods
    provided in this module
    """

    def set_attributes(fn):
        # add new tags to list of current tags
        # if no tags are present, create them
        for arg in args:
            curr_tags = getattr(fn, "tags", None)
            if curr_tags is None:
                setattr(fn, "tags", [arg])
            else:
                curr_tags.append(arg)
                setattr(fn, "tags", curr_tags)

        # any additional metadata
        for k, v in kwargs:
            setattr(fn, k, v)

    return set_attributes


def get_by_tag(tag):
    return [fn for fn in __SCENE_MAPPING if tag in getattr(fn, "tags", [])]



def __scenes_as_list():
    return list(__SCENE_MAPPING.values())


