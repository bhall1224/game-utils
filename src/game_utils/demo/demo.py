from game_utils import game, clock, screen

WIDTH = 1280
HEIGHT = 720

@game.run("bouncy-ball")
def event_handler(data, event, **config):
    return True

@game.screen_handler
@screen.screen_update("bouncy-ball")
def screen_update(data, settings, **config):
    return 0.0

@game.config
def config():
    return {}

@game.scene("bouncy-ball")
def update_sprites(dt, **config):
    return {}

@screen.screen_settings("bouncy-ball")
def get_screen_settings():
    return screen.ScreenSettings(
        width=WIDTH,
        height=HEIGHT,
        bg_color="black"
    )