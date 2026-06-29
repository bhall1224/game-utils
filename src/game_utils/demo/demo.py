#!/usr/bin/env python3

from game_utils import game, clock, screen, sprites
import pygame.draw as draw
from random import random
from pygame import Vector2, Surface, Rect, K_q, K_ESCAPE, K_a, K_d, K_s, K_w, QUIT
import pygame.key as key
import pygame.event as event

WIDTH = 1280
HEIGHT = 720
PUCK_SIZE = 40
SCENE = "bouncy-ball"

PLAYER = "striker"
PUCK = "puck"


@game.config
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
    }



def controller():    
    l, r, u, d, q, e = (key.get_pressed()[k] for k in [K_a, K_d, K_w, K_s, K_q, K_ESCAPE])

    if e or q:
        event.post(event.Event(QUIT))

    return Vector2((r - l), (d - u))


@sprites.player_sprite(PLAYER)
@game.get_config
def player_sprite(**config):
    return sprites.PlayerSprite(
        image=Surface((PUCK_SIZE, PUCK_SIZE)),
        position=Vector2(WIDTH / 4, HEIGHT / 2),
        controller=controller,
        physics_body=config[PLAYER]["physics_body"],
        boundaries=Rect(0, 0, WIDTH, HEIGHT),
    )


@sprites.sprite(PUCK)
@game.get_config
def player_sprite(**config):
    return sprites.PhysicsSprite(
        image=Surface((PUCK_SIZE, PUCK_SIZE)),
        position=Vector2(WIDTH / 2, HEIGHT / 2),
        physics_body=config[PUCK]["physics_body"],
        boundaries=Rect(0, 0, WIDTH, HEIGHT),
    )


@screen.screen_settings(SCENE)
def get_screen_settings():
    return screen.ScreenSettings(
        width=WIDTH,
        height=HEIGHT,
        title="Bouncy Ball",
    )


@game.screen_handler
@screen.screen_update(SCENE)
def screen_update(data, settings: screen.ScreenSettings, **config):
    player_settings = config[PLAYER]
    player_data = data[PLAYER]

    ball_settings = config[PUCK]
    ball_data = data[PUCK]

    table_settings = config["table"]

    # DRAW THE TABLE
    draw.rect(
        surface=settings.screen_surface,
        color=table_settings["color"],
        rect=(0, 0, settings.width, settings.height),
        border_radius=15,
    )
    # DRAW PLAYER
    draw.circle(
        surface=settings.screen_surface,
        color=player_settings["color"],
        center=player_data["position"],
        radius=player_settings["radius"],
    )

    # DRAW PUCK
    draw.circle(
        surface=settings.screen_surface,
        color=ball_settings["color"],
        center=ball_data["position"],
        radius=ball_settings["radius"],
    )

    return clock.get_delta_time()


@game.scene(SCENE)
@sprites.update_sprites
def update(dt, sprites, **config):
    # Physics and controller stuff happens here
    data_packet = {
        PLAYER: {"position": sprites[PLAYER].position},
        PUCK: {"position": sprites[PUCK].position},
    }

    sprites[PLAYER].position += (
        sprites[PLAYER].controller() * dt * config["controller"]["speed"]
    )

    return data_packet


@game.run(SCENE)
def event_handler(data, event, **config):
    return True
