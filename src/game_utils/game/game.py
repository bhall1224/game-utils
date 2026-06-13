
from collections.abc import Callable 
from typing import Any, Concatenate

import pygame

# module relies heavily on pygame
# initializing at module import insures
# everything is ready
pygame.init()

# TYPE ALIASES
##########################################################################################################

GameError = Exception
__FunctionType = Callable[Concatenate[float, ...], float]
__HandlerType = Callable[Concatenate[Any, ...], bool]


# CONSTANTS
##########################################################################################################

NEXT_UPDATE_EVENT = pygame.USEREVENT
NEXT_UPDATE_EVENT_ID = "next_scene_id"

__EVENT_HANDLER = "++event++"
__SCREEN_HANDLER = "++screen++"


# GLOBAL SETTINGS
##########################################################################################################

__function_mapping: dict[str, __FunctionType] = {}
__handler_mapping: dict[str, __HandlerType] = {}

# ANNOTATION METHODS
##########################################################################################################

def run(start_scene: str | None = None):
    """Main entry point for the game.  Annotate a method that sets the game configurations, and the game
    will start when you run the script with the Python interpreter.  No __name__ == "__main__" required.

    Args:
        start_scene (str | None, optional): The beginning scene. Defaults to None.

    Raises:
        GameError: An error raised during game play

    Returns:
        () -> Any: The annoted method
    """

    # annotated function returns config data or None
    def main(setup_func):
        try:
            config = setup_func() or {}
            running = True
            dt = 0.0

            screen_update_func = __handler_mapping.get(__SCREEN_HANDLER)
            event_handler_func = __handler_mapping[__EVENT_HANDLER]
            
            if start_scene is None:
                curr_scene = 0
                scenes = get_scenes_as_list()
            else:
                curr_scene = start_scene
                scenes = __function_mapping
            
            while running:                

                try:
                    screen_packet = scenes[curr_scene](dt, **config)
                except:
                    raise GameError("the game failed suddenly!")

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == NEXT_UPDATE_EVENT:
                        next_scene_name = event.dict.get(NEXT_UPDATE_EVENT_ID)

                        # if an ID is given, call the map
                        # otherwise we're working with a list
                        if next_scene_name is not None:
                            curr_scene = get_scene_by_name(next_scene_name)
                        else:
                            curr_scene += 1 
                    else:
                        running = event_handler_func(event, **config)                

                if screen_update_func is not None and not screen_update_func(screen_packet, **config):
                    raise GameError("screen activity error!")

            return setup_func
        except:
            raise GameError("The game failed suddenly!")
        
    return main

def scene(name=None) -> __FunctionType:
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
        return __add_function(fn, name)

    return add_scene

def event_handler(fn: __HandlerType) -> __HandlerType:
    """Register an event handler function by annotating a Python method with this annotation.

    Args:
        fn ((event, **config) -> bool): The annotated method

    Returns:
        (float, **config) -> float: A special callback function for handling events
    """
    return __add_handler(fn, __EVENT_HANDLER)

def screen_handler(fn: __HandlerType) -> __FunctionType:
    """Register a method for any screen handling logic
    (optional)

    Args:
        fn ((event, **config) -> bool): The annotated method

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
    return [fn for fn in __function_mapping if tag in getattr(fn, "tags", [])]

def get_scene_by_name(name):
    return __function_mapping.get(name)

def get_scenes_as_list():
    return list(__function_mapping.values())
    

# HELPER METHODS
##########################################################################################################

def __add_function(fn, name=None) -> __FunctionType:
    fn_name = name or chr(len(__function_mapping))
    __function_mapping[fn_name] = fn
    return fn

def __add_handler(fn, name) -> __HandlerType:
    __handler_mapping[name] = fn
    return fn