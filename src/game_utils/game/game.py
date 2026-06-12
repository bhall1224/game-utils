import pygame
from pygame.time import Clock
from abc import Callable

NEXT_UPDATE_EVENT = pygame.USEREVENT

__update_func_list: list[Callable[[float], None]] = []
__screen_update_func: Callable[[float], None] | None = None

__current_update_scene: int = 0
__frames_per_second = 60
__time_units = 1000

def main(event_handler_func: Callable[[pygame.event.Event], None]):
    if len(__update_func_list) == 0:
        raise NotImplementedError("need at least one update callback")
    clock = Clock()
    running = True
    dt = 0.0
    pygame.init()

    while running:
        dt = clock.tick(__frames_per_second) / __time_units
        
        if __screen_update_func is not None:
            __screen_update_func(dt)
        
        __update_func_list[__current_update_scene](dt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == NEXT_UPDATE_EVENT:
                __current_update_scene += 1
                if __current_update_scene >= len(__update_func_list):
                    raise IndexError("too many scene update events...")
            else:
                event_handler_func(event)



