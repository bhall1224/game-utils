from pygame.time import Clock

__CLOCK = Clock()

cdef float __get_dt_busy(float framerate, float units):
    return __CLOCK.tick_busy_loop(framerate) / units

cdef float __get_dt(float framerate, float units):
    return __CLOCK.tick(framerate) / units

def get_delta_time(framerate: float, units: float, busy_wait: bool = False) -> float:
    return __get_dt(framerate, units) if not busy_wait else __get_dt_busy(framerate, units)