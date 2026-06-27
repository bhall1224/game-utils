from game_utils import game, clock
import pygame.event

START_SCENE = "start-scene"
TEST_SCENE = "test-scene"
CONFIG_FLAG = "update-scene"
TEST_NAME = "Bee"
TEST_AGE = "Unknown"

def asserts_config(config):
    assert config is not None
    assert config["name"] == TEST_NAME
    assert config["age"] == TEST_AGE

def asserts_data(data):
    assert data is not None
    assert data.get("age") is not None
    assert isinstance(data["age"], int)

def update_scene(dt, **config):
    assert dt == 0.0
    asserts_config(config)

    if config.get(CONFIG_FLAG) is not None:
        pygame.event.post(
            pygame.event.Event(game.NEXT_UPDATE_EVENT, {game.NEXT_UPDATE_EVENT_ID: START_SCENE})
        )

    return {"age": 41}

def update_start_scene(dt, **config):
    asserts_config(config)

    if dt > 0.0:
        pygame.event.post(
            pygame.event.Event(game.NEXT_UPDATE_EVENT, {game.NEXT_UPDATE_EVENT_ID: TEST_SCENE})
        )
    
    return {"age": 1000, "name": "Dracula"}

def update_with_scene_name(dt, **config):
    asserts_config(config)
    if config.get(CONFIG_FLAG) is not None:
        assert dt > 0.0
        pygame.event.post(pygame.event.Event(pygame.QUIT))
    else:
        assert dt == 0.0
    return {"age": 0, "name": "Spider Man"}

def screen_handler_mock_no_dt(data, **config):
    asserts_config(config)
    asserts_data(data)
    return 0.0

def screen_handler_mock_with_dt(data, **config):
    asserts_config(config)
    asserts_data(data)

    return 0.0 if data.get("name") is None else clock.get_delta_time()

def mock_config():
    return {"name":TEST_NAME, "age":TEST_AGE}

def mock_config_with_dt():
    return {"name":TEST_NAME, "age":TEST_AGE, CONFIG_FLAG: 1}

def event_handle_test_update_flag(event, data, **config):
    asserts_config(config)
    asserts_data(data)
    assert event is not None
    assert event.type is not None
    return False

def event_handler_test_many_scenes(event, data, **config):
    asserts_config(config)
    asserts_data(data)
    assert event is not None
    assert event.type is not None
    assert event.dict is not None

    return True

def test_game():
    game.screen_handler(screen_handler_mock_no_dt)
    game.config(mock_config)
    game.scene()(update_scene)
    game.run()(event_handle_test_update_flag)

def test_game_with_start_scene():
    game.screen_handler(screen_handler_mock_no_dt)
    game.config(mock_config)
    game.scene(TEST_SCENE)(update_with_scene_name)
    game.run(TEST_SCENE)(event_handle_test_update_flag)

def test_game_with_many_scenes():
    game.screen_handler(screen_handler_mock_with_dt)
    game.config(mock_config_with_dt)
    game.scene()(update_scene)
    game.scene(START_SCENE)(update_start_scene)
    game.scene(TEST_SCENE)(update_with_scene_name)
    game.run()(event_handler_test_many_scenes)