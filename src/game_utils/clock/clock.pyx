from pygame.time import Clock

FRAMERATE_DEFAULT = 60.0
UNITS = 1000.0
__CLOCK = Clock()

cdef float __get_dt_busy(float framerate, float units):
    return __CLOCK.tick_busy_loop(framerate) / units

cdef float __get_dt(float framerate, float units):
    return __CLOCK.tick(framerate) / units

def get_delta_time(framerate: float = FRAMERATE_DEFAULT, units: float = UNITS, busy_wait: bool = True) -> float:
    return __get_dt_busy(framerate, units) if busy_wait else __get_dt(framerate, units)