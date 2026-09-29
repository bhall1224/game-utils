import pygame
import pytest
from game_utils.game import Game
from game_utils.screen.screen import ScreenSettings
from game_utils.sprites import Sprites
from game_utils.sprites.sprites import GameSprite


# TEST 1 - NO SCREEN NO SPRITES
def config_asserts(config):
    assert config is not None
    assert len(config) > 0
    assert config.get("data") is not None
    assert config["data"] == {"id": 1234}


def event_asserts(event):
    assert event is not None
    assert event.type is not None
    assert event.dict is not None


@pytest.fixture
def game_fixture():

    testgame = Game()
    yield testgame
    testgame.quit()


def mock_config():
    return {"data": {"id": 1234}}


def mock_event_handler_asserts(event, settings, config):
    assert settings is not None
    assert settings.dimensions() is None
    assert settings.screen() is None

    config_asserts(config)
    event_asserts(event)
    return False


def test_game_no_screen(game_fixture):
    game_fixture.config(mock_config)
    game_fixture.event_handler(mock_event_handler_asserts)
    game_fixture.run(screen=False)


# TEST 2 - MOCK SCREEN WITH SPRITES


TEST_PLAYER = "PLAYER"


@pytest.fixture
def game_fixture2():
    testgame2 = Game()
    yield testgame2
    testgame2.quit()


@pytest.fixture
def sprites():
    return Sprites()


def mock_screen_settings(config):
    return ScreenSettings(title="Mock Game", dimensions=pygame.Vector2(1.0, 1.0))


def mock_sprite():
    return GameSprite(
        image=pygame.Surface((1.0, 1.0)), position=pygame.Vector2(1.0, 1.0)
    )


def mock_event_handler_with_sprites(event, settings, sprites, config):
    assert sprites is not None
    assert len(sprites) > 0
    assert sprites.get(TEST_PLAYER) is not None

    assert settings is not None
    assert settings.dimensions() is not None
    assert settings.dimensions() == pygame.Vector2(1.0, 1.0)

    assert settings.screen() is None

    event_asserts(event)
    config_asserts(config)

    return False


def test_game_mock_screen_with_sprites(game_fixture2, sprites):
    game_fixture2.config(mock_config)
    game_fixture2.screen_settings(mock_screen_settings)
    game_fixture2.event_handler(sprites.sprites(mock_event_handler_with_sprites))
    sprites.add(TEST_PLAYER)(mock_sprite)
    game_fixture2.run(screen=False)
