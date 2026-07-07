from typing import Any
import os
import pygame
import json

# module relies heavily on pygame
# initializing at module import insures
# everything is ready
if not pygame.get_init():
    print("pygame not initialized, initializing now...")
    pygame.init()

# TYPE ALIASES
##########################################################################################################

GameError = Exception

# CONSTANTS
##########################################################################################################

NEXT_UPDATE_EVENT = pygame.USEREVENT
NEXT_UPDATE_EVENT_ID = "next_scene_id"

__CONFIG = "++config++"
__SCREEN_HANDLER = "++screen++"

# GLOBAL SETTINGS
##########################################################################################################

__scene_mapping: dict[str, Any] = {}
__handler_mapping: dict[str, Any] = {}

# ANNOTATION METHODS
##########################################################################################################


def run(*scenes: str):
    """Main entry point for the game.  Annotate a method that sets the game configurations, and the game
    will start when you run the script with the Python interpreter.  No __name__ == "__main__" required.

    Args:
        title (str | None, optional): The title of the game window. Defaults to None.
        *scenes (str): The scenes to include in the game.

    Raises:
        GameError: An error raised during game play

    Returns:
        () -> Any: The annoted method
    """

    # annotated function returns config data or None
    def main(event_handler_func):
        running = True
        dt = 0.0
        i = 0

        # get optional screen update function
        screen_update_func = __handler_mapping.get(__SCREEN_HANDLER)

        # get optional config function
        config = __handler_mapping.get(__CONFIG, lambda: {})()

        # first scene is either the scene given or the first one in the mapping
        curr_scene = __get_default_scene(scenes, i)

        while running:
            try:
                scene_fn = __scene_mapping[curr_scene]
            except KeyError:
                raise GameError(f"scene not found! scene: {curr_scene}")

            data_packet = scene_fn(dt, **config)

            if screen_update_func is not None:
                dt = screen_update_func(data_packet, **config)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == NEXT_UPDATE_EVENT:
                    try:
                        if event.dict.get(NEXT_UPDATE_EVENT_ID) is not None:
                            curr_scene = event.dict[NEXT_UPDATE_EVENT_ID]
                        else:
                            i += 1
                            curr_scene = __get_default_scene(scenes, i)
                    except KeyError:
                        raise GameError(f"next scene not given! event: {event}")
                else:
                    running = event_handler_func(event, data_packet, **config)

        return event_handler_func

    return main


def scene(name=None):
    """Decorate a method to register it as a scene.  A scene is basically an update
    function that will be called once per game loop.  You may register as many as you wish.
    These are inteded for game logic that relies on the change in time, and serve as an entry
    point to your logic.

    Args:
        name (str, optional): Pass an optional name for the scene, which will be added as a tag.
    Defaults to None.
    """

    # inner method simply registers the function in the map
    def add_scene(fn):
        return __add_scene(fn, name)

    return add_scene


def config(
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
            config = fn()
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

            return config

        return __add_handler(__wrapper, __CONFIG)
    return __inner


def screen_handler(fn):
    """Register a method for any screen handling logic
    (optional)

    Args:
        fn ((data, **config) -> bool): The annotated method

    Returns:
        (float, **config) -> float: A special callback function for handling screen events
    """
    return __add_handler(fn, __SCREEN_HANDLER)


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


# ACCESS METHODS
##########################################################################################################


def get_by_tag(tag):
    return [fn for fn in __scene_mapping if tag in getattr(fn, "tags", [])]


def inject_config(key=None):
    def __inner(fn):
        def __wrapper(*args):
            config = __handler_mapping.get(__CONFIG, lambda: {})()
            config = config.get(key) if key is not None else config
            return fn(*args, **config)
        return __wrapper
    return __inner


# HELPER METHODS
##########################################################################################################
def __get_default_scene(scenes, i):
    return list(__scene_mapping.keys())[i] if len(scenes) == 0 else scenes[i]


def __add_scene(fn, name):
    fn_name = name or fn.__name__
    __scene_mapping[fn_name] = fn
    return fn


def __add_handler(fn, name):
    __handler_mapping[name] = fn
    return fn
