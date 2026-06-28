from game_utils import game, screen
import pygame.display as display

class screen_mock:

    def get_width(self):
        return 0.0
    def get_height(self):
        return 0.0
    
class display_mock:
        
    def set_mode(*args):
        return screen_mock()
    
    def flip():
        pass

    def set_caption(caption):
        pass

def test_screen():
    screen.screen_settings("test")(lambda: screen.ScreenSettings(display_mod=display_mock))
    game.screen_handler(
        screen.screen_update("test")(lambda data, settings, **config: 0.0)
    )
    game.scene("test")(lambda dt, **config: {"foo": 1, "bar": 'e'})

    game.run("test")(lambda data, event, **config: False)