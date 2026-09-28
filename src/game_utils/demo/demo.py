#!/usr/bin/env python3

from game_utils.game import Game
from game_utils import sprites
from game_utils import screen
from game_utils import clock
from game_utils import controller
import pygame

from game_utils.physics import PhysicsBody

# Constant defaults for screen refresh
FRAMERATE = 60.0
UNITS = 1000.0  # pygame clock returns ms - take s as default

WIDTH = 1280
HEIGHT = 720
PUCK_SIZE = 40

PLAYER = "player"
PUCK = "puck"

CONTROLLER_VECTOR = "acceleration"
CONTROLLER_EVENT = pygame.USEREVENT

bouncyball = Game()
bouncyball_sprites = sprites.Sprites()
bouncyball_controllers = controller.Controllers()


@bouncyball.config()
def config():
    return {
        PLAYER: {
            "color": "darkred",
            "physics_body": {"mass": 4.0, "friction": 0.002, "elasticity": 0.0},
            "radius": PUCK_SIZE,
        },
        PUCK: {
            "color": "midnightblue",
            "physics_body": {"mass": 0.5, "friction": 0.0, "elasticity": 0.0},
            "radius": PUCK_SIZE,
        },
        "controller": {"speed": 200.0},
        "table": {"color": "firebrick"},
        "title": "Bouncy Ball",
    }

@bouncyball.inject_config
def player_controller(config):
    l, r, u, d, q, e = (
        pygame.key.get_pressed()[k]
        for k in [
            pygame.K_a,
            pygame.K_d,
            pygame.K_w,
            pygame.K_s,
            pygame.K_q,
            pygame.K_ESCAPE,
        ]
    )

    if e or q:
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    new_position = (
        pygame.Vector2((r - l), (d - u))
        * config["controller"]["speed"]
        * clock.get_delta_time(framerate=FRAMERATE, units=UNITS)
    )

    pygame.event.post(pygame.event.Event(CONTROLLER_EVENT, {CONTROLLER_VECTOR: new_position}))


@bouncyball_sprites.add(PLAYER)
@bouncyball.inject_config
def player_sprite(config):
    player_body = config[PLAYER]["physics_body"]
    return sprites.GameSprite(
        image=pygame.Surface((PUCK_SIZE, PUCK_SIZE)),
        position=pygame.Vector2(WIDTH / 4, HEIGHT / 2),
        physics_body=PhysicsBody(
            mass=player_body["mass"],
            position=player_body["position"],
            friction=player_body["friction"],
            elasticity=player_body["elasticity"]
        ),
    )


@bouncyball_sprites.add(PUCK)
@bouncyball.inject_config
def puck_sprite(config):
    puck_body = config[PLAYER]["physics_body"]
    return sprites.PhysicsSprite(
        image=pygame.Surface((PUCK_SIZE, PUCK_SIZE)),
        position=pygame.Vector2(WIDTH / 2, HEIGHT / 2),
        physics_body=PhysicsBody(
                    mass=puck_body["mass"],
                    position=puck_body["position"],
                    friction=puck_body["friction"],
                    elasticity=puck_body["elasticity"]
                ),
    )


@bouncyball.screen_settings()
@bouncyball.inject_config
def screen_settings(config):
    return screen.ScreenSettings(
        dimensions=pygame.Vector2(WIDTH, HEIGHT),
        title=config["title"],
    )


def screen_update(sprites, settings, config):
    player_settings = config[PLAYER]
    player_data = sprites[PLAYER]

    ball_settings = config[PUCK]
    ball_data = sprites[PUCK]

    table_settings = config["table"]

    # DRAW THE TABLE
    pygame.draw.rect(
        surface=settings.__screen_surface,
        color=table_settings["color"],
        rect=(0, 0, settings.width, settings.height),
        border_radius=15,
    )
    # DRAW PLAYER
    pygame.draw.circle(
        surface=settings.__screen_surface,
        color=player_settings["color"],
        center=player_data.get_rect(),
        radius=player_settings["radius"],
    )

    # DRAW PUCK
    pygame.draw.circle(
        surface=settings.__screen_surface,
        color=ball_settings["color"],
        center=ball_data.get_rect(),
        radius=ball_settings["radius"],
    )


@bouncyball.event_handler
@bouncyball_sprites.sprites
def event_handler(event, sprites, settings, config):
    # LOGIC GOES HERE -- Called once per game loop
    if event.type == CONTROLLER_EVENT:
        new_vector = event.dict[CONTROLLER_VECTOR]
        sprites[PLAYER].physics_body.apply_force(new_vector, clock.get_delta_time())

    screen_update(sprites, settings, config)
    return True


if __name__ == "__main__":
    bouncyball.run()