from pygame import Vector2, Surface

from game_utils.game import Game
from game_utils.screen import ScreenSettings
from game_utils.sprites import GameSprite, Sprites

TEST_PLAYER = "PLAYER"

testgame = Game()
testgame2 = Game()

@testgame.config
@testgame2.config
def mock_config():
    return {
        "data": 1234
    }

@testgame.event_handler
def mock_event_handler_asserts(event, settings, config):
    assert event is not None
    assert event.type is not None
    assert event.dict is not None

    assert settings is not None
    assert settings.dimensions is None

    assert config is not None
    assert len(config) > 0
    assert config.get("data") is not None
    assert config["data"] == {"id": 1234}

def test_game_no_screen():
    testgame.run(screen=False)


test_sprites = Sprites()

@testgame2.screen_settings()
def mock_screen_settings(config):
    return ScreenSettings(title="Mock Game", dimensions=Vector2(1.0, 1.0))

@test_sprites.add("test")
def mock_sprite():
    return GameSprite(image=Surface(1.0, 1.0), position=Vector2(1.0, 1.0))

@testgame2.event_handler
@test_sprites.sprites
def mock_event_handler_with_sprites(event, settings, sprites, config):
    mock_event_handler_asserts(event, settings, config)

    assert sprites is not None
    assert len(sprites) > 0
    assert sprites.get(TEST_PLAYER) is not None

def test_game_no_screen_with_sprites():
    testgame2.run(screen=False)