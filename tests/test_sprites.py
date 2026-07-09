import pytest
from pygame import Rect, Surface, Vector2

import game_utils.sprites.sprites as sprite_module
from game_utils.sprites import (
    GameSprite,
    PhysicsSprite,
    PlayerSprite,
    inject_sprites,
    player_sprite,
    sprite,
    sprite_group,
)


@pytest.fixture(autouse=True)
def clear_sprite_registry():
    """Reset sprite registries before and after each test."""
    sprite_module.__SPRITES.clear()
    sprite_module.__SPRITE_GROUPS.clear()
    yield
    sprite_module.__SPRITES.clear()
    sprite_module.__SPRITE_GROUPS.clear()


@pytest.fixture
def test_surface():
    """Create a small surface for sprite tests."""
    return Surface((16, 16))


def test_game_sprite_initializes_rect_position_and_boundaries(test_surface):
    """GameSprite should store image details and derive rect information."""
    position = Vector2(12, 18)
    boundaries = Rect(0, 0, 100, 100)

    sprite = GameSprite(test_surface, position, boundaries)

    assert sprite.image is test_surface
    assert sprite.position == position
    assert sprite.boundaries == boundaries
    assert sprite.rect.topleft == (12, 18)
    assert sprite.rect.size == (16, 16)


def test_physics_and_player_sprites_store_dependencies(test_surface):
    """Physics and player sprites should retain their injected dependencies."""
    physics_body = object()
    controller = object()

    physics_sprite = PhysicsSprite(test_surface, Vector2(3, 4), physics_body)
    player_sprite_instance = PlayerSprite(
        test_surface,
        Vector2(5, 6),
        controller,
        physics_body,
        Rect(0, 0, 50, 50),
    )

    assert physics_sprite.physics_body is physics_body
    assert player_sprite_instance.physics_body is physics_body
    assert player_sprite_instance.controller is controller
    assert player_sprite_instance.boundaries == Rect(0, 0, 50, 50)


def test_sprite_decorator_registers_sprite_by_name(test_surface):
    """The sprite decorator should register the created sprite in the global map."""

    @sprite("hero")
    def build_hero():
        return GameSprite(test_surface, Vector2(1, 2))

    assert build_hero is not None
    assert "hero" in sprite_module.__SPRITES
    assert isinstance(sprite_module.__SPRITES["hero"], GameSprite)


def test_player_sprite_decorator_uses_player_sprite_registry(test_surface):
    """The player_sprite decorator should behave like sprite but keep player sprites."""

    @player_sprite("player-one")
    def build_player():
        return PlayerSprite(test_surface, Vector2(4, 5), object(), object())

    assert "player-one" in sprite_module.__SPRITES
    assert isinstance(sprite_module.__SPRITES["player-one"], PlayerSprite)


def test_inject_sprites_passes_registry_to_wrapped_function(test_surface):
    """The inject_sprites wrapper should supply the sprite registry to the wrapped function."""

    @sprite("named-sprite")
    def build_named_sprite():
        return GameSprite(test_surface, Vector2(7, 8))

    @inject_sprites
    def wrapped(dt, sprites, **config):
        assert dt == 0.25
        assert sprites is sprite_module.__SPRITES
        assert config["name"] == "demo"
        return sprites["named-sprite"]

    result = wrapped(0.25, name="demo")

    assert result is sprite_module.__SPRITES["named-sprite"]


def test_sprite_group_registers_group_and_sprites(test_surface):
    """Sprite groups should be stored and populated from the decorated mapping."""

    @sprite_group("team")
    def build_team():
        return {
            "hero": GameSprite(test_surface, Vector2(0, 0)),
            "enemy": GameSprite(test_surface, Vector2(5, 5)),
        }

    assert "team" in sprite_module.__SPRITE_GROUPS
    assert len(sprite_module.__SPRITE_GROUPS["team"]) == 2
    assert sprite_module.__SPRITES["hero"].rect.topleft == (0, 0)
    assert sprite_module.__SPRITES["enemy"].rect.topleft == (5, 5)

