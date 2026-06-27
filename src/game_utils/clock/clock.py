from pygame.time import Clock

FRAMERATE_DEFAULT = 60.0
UNITS = 1000.0
__CLOCK = Clock()

def __get_dt_busy(framerate, units):
    return __CLOCK.tick_busy_loop(framerate) / units

def __get_dt(framerate, units):
    return __CLOCK.tick(framerate) / units

def get_delta_time(framerate: float = FRAMERATE_DEFAULT, units: float = UNITS, busy_wait: bool = True) -> float:
    return __get_dt_busy(framerate, units) if busy_wait else __get_dt(framerate, units)