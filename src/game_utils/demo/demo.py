#!/usr/bin/env python3

from game_utils import game, clock, screen
import pygame.draw as draw
from random import random
from pygame import Vector2

WIDTH = 1280
HEIGHT = 720
PUCK_SIZE = 40
SCENE = "bouncy-ball"

player_positions = [Vector2(WIDTH/4, HEIGHT/2)]
puck_positions = [Vector2(3*WIDTH/4, HEIGHT/2)]

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
    player_settings = config["player"]
    player_data = data["player"]

    ball_settings = config["puck"]
    ball_data = data["puck"]

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

@game.config
def config():
    return {
        "player": {
            "color": "darkred",
            "physics_body": {"mass": 4, "friction": 0.002, "elasticity": 0},
            "radius": PUCK_SIZE
        },
        "puck": {
            "color": "midnightblue",
            "physics_body": {"mass": 0.5, "friction": 0, "elasticity": 0},
            "radius": PUCK_SIZE
        },
        "controller": {"speed": 1500.0},
        "table": {"color": "firebrick"},
    }

@game.scene(SCENE)
def update(dt, **config):
    def new_coord(coord: float):
        neg = random() > 0.5
        return coord + config["controller"]["speed"] * dt * random() * (-1 if neg else 1)
    
    def new_pos(pos):
        return Vector2(new_coord(pos.x), new_coord(pos.y))
    
    data_packet = {
        "player": {
            "position": player_positions[-1]
        },
        "puck": {
            "position": puck_positions[-1]
        },
    }

    player_positions.append(new_pos(player_positions[-1]))
    puck_positions.append(new_pos(puck_positions[-1]))

    return data_packet


@game.run(SCENE)
def event_handler(data, event, **config):
    return True