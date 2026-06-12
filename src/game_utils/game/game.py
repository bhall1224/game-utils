import pygame
from abc import Callable

NEXT_UPDATE_EVENT = pygame.USEREVENT

__update_func_list: list[Callable[[float], None]] = []
__screen_update_func: Callable[[float], float] | None = None

def main(event_handler_func: Callable[[pygame.event.Event, float], bool]):
    """Decorate the main event handler for the game

    Args:
        event_handler_func (Callable[[pygame.event.Event, float], bool]): _description_

    Raises:
        NotImplementedError: _description_
        IndexError: _description_
    """
    if len(__update_func_list) == 0:
        raise NotImplementedError("need at least one update callback")
    
    running = True
    dt = 0.0
    pygame.init()

    while running:
        if __screen_update_func is not None:
            dt = __screen_update_func(dt)
        
        __update_func_list[__current_update_scene](dt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == NEXT_UPDATE_EVENT:
                __current_update_scene += 1
                if __current_update_scene >= len(__update_func_list):
                    raise IndexError("too many scene update events...")
            else:
                running = event_handler_func(event, dt)


def update(func: Callable[[float], None], insert: int = 0):
    __update_func_list.insert(insert, func)