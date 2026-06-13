from game_utils import game


@game.scene("test-scene")
def update(dt, **config):
    assert dt == 0.0
    assert config is not None
    print(f"{config["name"]}'s age is {config["age"]}")
    return {"age": 41}

@game.event_handler
def event_handle_test_update_flag(event, **config):
    print("event handler")
    assert event is not None
    assert event.type is not None
    assert config["name"] == "Bee"
    assert config["age"] == "Unknown"
    return False

@game.screen_handler
def screen_handler_mock(data, **config):
    print("screen handler")
    assert config["name"] == "Bee"
    assert data is not None
    assert data["age"] == 41

    print(f"{config['name']}'s actual age is {data['age']}")
    return True


@game.run()
def test_run():
    return {"name":"Bee", "age":"Unknown"}
