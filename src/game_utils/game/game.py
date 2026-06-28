
from typing import Any

import pygame

# module relies heavily on pygame
# initializing at module import insures
# everything is ready
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
    def main(event_handler_func):
        running = True
        dt = 0.0

        # get optional screen update function
        screen_update_func = __handler_mapping.get(__SCREEN_HANDLER)   
        
        # get optional config function
        config = __handler_mapping.get(__CONFIG, lambda: {})()

        # first scene is either the scene given or the first one in the mapping
        curr_scene = start_scene or list(__scene_mapping.keys())[0]
                    
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
                        curr_scene = event.dict[NEXT_UPDATE_EVENT_ID]
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

def config(fn):
    """Register a handler function for returning configurations by annotating a Python method with this annotation.

    Args:
        fn (() -> Any): The annotated method

    Returns:
        (float, **config) -> float: A special callback function for handling events
    """
    return __add_handler(fn, __CONFIG)

def screen_handler(fn):
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
    return [fn for fn in __scene_mapping if tag in getattr(fn, "tags", [])]
    

# HELPER METHODS
##########################################################################################################

def __add_scene(fn, name):
    fn_name = name or str(len(__scene_mapping.items()))
    __scene_mapping[fn_name] = fn
    return fn

def __add_handler(fn, name):
    __handler_mapping[name] = fn
    return fn