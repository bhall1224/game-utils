from collections.abc import Callable
from typing import Any

# ========== Type Aliases ==========
GameRunEventHandler = Callable[..., bool]

import pytest
from game_utils import game, clock
import pygame.event

# ========== Constants ==========
START_SCENE = "start-scene"
TEST_SCENE = "test-scene"
TRIGGER_SCENE_CHANGE_FLAG = "update-scene"
TEST_NAME = "Bee"
TEST_AGE = "Unknown"



# ========== Config Assertions ==========
def asserts_config(config):
    """Verify config has required test values."""
    assert config is not None
    assert config["name"] == TEST_NAME
    assert config["age"] == TEST_AGE


def asserts_data(data):
    """Verify data structure is valid."""
    assert data is not None
    assert data.get("age") is not None
    assert isinstance(data["age"], int)


# ========== Mock Scene Handlers ==========
def update_test_scene(dt, **config):
    """Update handler for initial test scene. Optionally triggers scene transition."""
    assert dt == 0.0
    asserts_config(config)

    if config.get(TRIGGER_SCENE_CHANGE_FLAG) is not None:
        pygame.event.post(
            pygame.event.Event(game.NEXT_UPDATE_EVENT, {game.NEXT_UPDATE_EVENT_ID: START_SCENE})
        )

    return {"age": 42}


def update_start_scene(dt, **config):
    """Update handler for start scene. Triggers transition to test scene when dt > 0."""
    asserts_config(config)

    if dt > 0.0:
        pygame.event.post(
            pygame.event.Event(game.NEXT_UPDATE_EVENT, {game.NEXT_UPDATE_EVENT_ID: TEST_SCENE})
        )
    
    return {"age": 1000, "name": "Dracula"}


def update_scene_with_transitions(dt, **config):
    """Update handler that conditionally triggers transitions based on config and dt."""
    asserts_config(config)
    if config.get(TRIGGER_SCENE_CHANGE_FLAG) is not None:
        assert dt > 0.0
        pygame.event.post(pygame.event.Event(pygame.QUIT))
    else:
        assert dt == 0.0
    return {"age": 0, "name": "Spider Man"}


# ========== Mock Screen Handlers ==========
def screen_handler_returns_zero_delta(data, **config):
    """Screen handler that always returns 0.0 delta time."""
    asserts_config(config)
    asserts_data(data)
    return 0.0


def screen_handler_uses_real_delta(data, **config):
    """Screen handler that returns real delta time when name is present in data."""
    asserts_config(config)
    asserts_data(data)
    return 0.0 if data.get("name") is None else clock.get_delta_time()


# ========== Mock Event Handlers ==========
def event_handler_basic(event, data, **config):
    """Basic event handler that verifies event and config, returns False to continue."""
    asserts_config(config)
    asserts_data(data)
    assert event is not None
    assert event.type is not None
    return False


def event_handler_with_scene_transitions(event, data, **config):
    """Event handler that validates full event structure for multi-scene testing."""
    asserts_config(config)
    asserts_data(data)
    assert event is not None
    assert event.type is not None
    assert event.dict is not None
    return True


# ========== Config Factories ==========
def create_basic_config():
    """Create basic test config without scene transition trigger."""
    return {"name": TEST_NAME, "age": TEST_AGE}


def create_config_with_scene_trigger():
    """Create config that triggers scene transitions."""
    return {"name": TEST_NAME, "age": TEST_AGE, TRIGGER_SCENE_CHANGE_FLAG: 1}


# ========== Fixtures ==========
@pytest.fixture
def basic_game_setup():
    """Setup: screen handler, config, default scene, event handler."""
    game.screen_handler(screen_handler_returns_zero_delta)
    game.config()(create_basic_config)
    return None


@pytest.fixture
def multi_scene_game_setup():
    """Setup: screen handler with delta time, config with trigger, multiple scenes."""
    game.screen_handler(screen_handler_uses_real_delta)
    game.config()(create_config_with_scene_trigger)
    return None


# ========== Tests ==========
def test_basic_game_initialization(basic_game_setup):
    """
    Test: Game initializes correctly with default scene and returns control flow.
    - Verifies config is passed to scene update
    - Verifies scene returns valid data
    - Verifies event handler receives events
    """
    game.scene()(update_test_scene)
    result: GameRunEventHandler = game.run()(event_handler_basic)
    
    # Verify game.run() completed without error (result should not raise)
    assert callable(result)


def test_game_with_named_start_scene(basic_game_setup):
    """
    Test: Game can initialize with a specific named start scene.
    - Verifies initial scene name is respected
    - Verifies proper scene handler is invoked
    """
    game.scene(TEST_SCENE)(update_scene_with_transitions)
    result: GameRunEventHandler = game.run(TEST_SCENE)(event_handler_basic)
    
    assert callable(result)


def test_game_with_scene_transitions(multi_scene_game_setup):
    """
    Test: Game supports multiple scenes with transitions between them.
    - Verifies initial scene is set correctly
    - Verifies scene registration and transition capability
    - Verifies event handler works with scene transitions
    """
    # Register three scenes
    game.scene()(update_test_scene)
    game.scene(START_SCENE)(update_start_scene)
    game.scene(TEST_SCENE)(update_scene_with_transitions)
    
    # Run game from start scene, should handle transitions
    result: GameRunEventHandler = game.run(START_SCENE)(event_handler_with_scene_transitions)
    
    assert callable(result)


def test_screen_handler_receives_data():
    """
    Test: Screen handler receives valid scene data.
    - Verifies screen handler is invoked with data from scene update
    - Verifies delta time is properly returned
    """
    screen_handler_called = False
    received_data = None
    
    def tracking_screen_handler(data, **config):
        nonlocal screen_handler_called, received_data
        screen_handler_called = True
        received_data = data
        asserts_config(config)
        asserts_data(data)
        return 0.0
    
    game.screen_handler(tracking_screen_handler)
    game.config()(create_basic_config)
    game.scene()(update_test_scene)
    game.run()(event_handler_basic)
    
    assert screen_handler_called, "Screen handler should be called"
    assert received_data is not None
    assert received_data.get("age") == 42


def test_event_handler_receives_events():
    """
    Test: Event handler is invoked and can process events.
    - Verifies event handler receives pygame events
    - Verifies it receives updated scene data
    """
    event_handler_called = False
    
    def tracking_event_handler(event, data, **config):
        nonlocal event_handler_called
        event_handler_called = True
        asserts_config(config)
        asserts_data(data)
        assert event is not None
        return False
    
    game.screen_handler(screen_handler_returns_zero_delta)
    game.config()(create_basic_config)
    game.scene()(update_test_scene)
    game.run()(tracking_event_handler)
    
    assert event_handler_called, "Event handler should be called"


def test_config_passed_through_pipeline():
    """
    Test: Config is passed through scene and screen handlers.
    - Verifies config propagates to all handlers
    - Verifies config values are preserved
    """
    configs_received = []
    
    def tracking_scene_update(dt, **config):
        configs_received.append(("scene", config))
        asserts_config(config)
        return {"age": 42}
    
    def tracking_screen_handler(data, **config):
        configs_received.append(("screen", config))
        asserts_config(config)
        return 0.0
    
    def tracking_event_handler(event, data, **config):
        configs_received.append(("event", config))
        asserts_config(config)
        return False
    
    game.screen_handler(tracking_screen_handler)
    game.config()(create_basic_config)
    game.scene()(tracking_scene_update)
    game.run()(tracking_event_handler)
    
    # Verify config was received by multiple handlers
    assert len(configs_received) >= 2, "Config should be passed to multiple handlers"
    for handler_name, config in configs_received:
        assert config["name"] == TEST_NAME
        assert config["age"] == TEST_AGE