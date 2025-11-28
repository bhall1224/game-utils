#!/usr/bin/env python3
from typing import Any, Literal

import pygame.display as display
import pygame.draw as draw
import pygame.event
import pygame.sprite as sprite
from pygame import Rect, Surface, Vector2

from .controller import DEFAULT_KEYBOARD_ACTIONS, DefaultKeyboardController
from .game import SpriteGame
from .physics import PhysicsBody
from .screen import ScreenSettings
from .sprites import PhysicsSprite, PlayerSprite
from .vector_utils import apply_vector_actions, get_random_vector


class BouncyBallPlayer(PlayerSprite):
    def __init__(
        self,
        image: Surface,
        position: Vector2,
        controller: DefaultKeyboardController,
        color: str = "indigo",
        physics_body: PhysicsBody = PhysicsBody(),
        boundaries: Rect | None = None,
        id: int = 0,
    ):
        super().__init__(image, position, controller, physics_body, boundaries, id)
        self.collided = False
        self.color = color

    def update(self, *args: Any, **kwargs: Any):
        dt = args[0]

        # sync position and physics body
        accel = self.controller.direction()
        self.physics_body.force(accel, dt)

        # bound positions
        self._update_pos(
            self.physics_body.position,
            xbounds=self._bounds_x,
            ybounds=self._bounds_y,
        )

        if self.controller.action(DefaultKeyboardController.Commands.QUIT.value) > 0.0:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def _bounds_x(self):
        self.physics_body.velociy = apply_vector_actions(
            self.physics_body.velociy,
            lambda v: Vector2(0, v.y),
        )

    def _bounds_y(self):
        self.physics_body.velociy = apply_vector_actions(
            self.physics_body.velociy,
            lambda v: Vector2(v.x, 0),
        )

    def _apply_controller_force(self, force: Vector2, dt: float):
        force /= dt if dt > 0 else 1
        self.physics_body.force(force, dt)


class BouncyBallPuck(PhysicsSprite):
    def __init__(
        self,
        image: Surface,
        position: Vector2,
        physics_body: PhysicsBody,
        color: str = "blue",
        boundaries: Rect | None = None,
        id: int = 0,
        speed: float = 50,
    ):
        super().__init__(image, position, physics_body, boundaries, id)
        self.color = color
        self.speed = speed
        self.collided = False
        self.physics_body.velociy = get_random_vector(speed)
        self.start_position = Vector2.copy(position)

    def update(self, *args: Any, **kwargs: Any):
        reset = kwargs.get("reset")
        if reset is not None:
            self.reset(position=reset)
        collided = kwargs.get("collided")
        if collided is not None:
            self.collided = True

        # sync position and physics body
        # bound positions
        self._update_pos(
            self.physics_body.position,
            xbounds=self.__bounds_x,
            ybounds=self.__bounds_y,
        )

    def __bounds_x(self):
        self.physics_body.velociy = (
            apply_vector_actions(
                self.physics_body.velociy, lambda v: Vector2(-v.x, v.y)
            )
            * self.physics_body.elasticity
        )

    def __bounds_y(self):
        self.physics_body.velociy = (
            apply_vector_actions(
                self.physics_body.velociy,
                lambda v: Vector2(v.x, -v.y),
            )
            * self.physics_body.elasticity
        )


class BouncyBallSettings(ScreenSettings):
    def __init__(
        self,
        player,
        puck,
        *,
        width=0,
        height=0,
        frames_per_second=60,
        bg_color=None,
        bg_image=None,
    ):
        super().__init__(
            width=width,
            height=height,
            frames_per_second=frames_per_second,
            bg_color=bg_color,
            bg_image=bg_image,
        )
        self.puck = puck
        self.player = player

    def update_screen(self):
        # DRAW THE TABLE
        draw.rect(
            surface=self.screen,
            color=self.bg_color,
            rect=(0, 0, self.width, self.height),
            border_radius=15,
        )
        # DRAW PLAYER
        draw.circle(
            self.screen,
            self.player.color,
            self.player.position,
            self.player.rect.h,
        )

        # DRAW PUCK
        draw.circle(
            self.screen,
            self.puck.color,
            self.puck.position,
            self.puck.rect.h,
        )


class BouncyBall(SpriteGame):
    def __init__(
        self,
        settings: ScreenSettings,
        player_sprite: BouncyBallPlayer,
        *other_sprites: BouncyBallPuck,
    ):
        # configure sprites
        super().__init__(settings, player_sprite, *other_sprites)
        # overloads type
        self.puck = other_sprites[0]
        self.player_sprite = player_sprite
        display.set_caption("Air Hockey")

    def _update(self):
        self._update_sprites()

    def __update_player(self):
        self.player_sprite.update(self.dt)

    def __update_puck(self):
        self.puck.physics_body.move(self.dt)
        self.puck.update()

    def _update_sprites(self):
        self.__update_player()
        self.__update_puck()
        self.__update_collisions()

    def __update_collisions(self):

        if sprite.collide_circle(self.player_sprite, self.puck):
            if not self.player_sprite.collided:
                self.player_sprite.physics_body.on_collide(self.puck.physics_body)
                self.puck.physics_body.on_collide(self.player_sprite.physics_body)
                self.player_sprite.collided = True
        else:
            self.player_sprite.collided = False


if __name__ == "__main__":
    import json
    import os

    path = os.path.dirname(os.path.relpath(__file__))
    with open(
        os.path.join(path, ".config", "demo.json"),
        mode="r",
        encoding="utf-8",
    ) as input_file:
        input_params = json.load(input_file)

        screen = input_params["screen"]
        controller = input_params["controller"]
        player_data = input_params["player"]
        puck_data = input_params["puck"]
        table_color = input_params["table"]["color"]

        ctrl_speed = controller["speed"]
        player_physics = player_data["physics_body"]
        player_color = player_data["color"]
        puck_physics = puck_data["physics_body"]
        puck_color = puck_data["color"]

        screen_w = screen["width"]
        screen_h = screen_w / 16 * 9  # screen["height"]

        puck_size = screen_h / 9 / 2
        player = BouncyBallPlayer(
            image=Surface((puck_size, puck_size)),
            position=Vector2(screen_w / 2, screen_h / 2),
            controller=DefaultKeyboardController(
                float(ctrl_speed), *DEFAULT_KEYBOARD_ACTIONS
            ),
            physics_body=PhysicsBody(
                mass=player_physics["mass"],
                friction=player_physics["friction"],
                elasticity=player_physics["elasticity"],
            ),
            boundaries=Rect(screen_w, 0, screen_h, 0),
            color=player_color,
        )

        puck = BouncyBallPuck(
            image=Surface((puck_size, puck_size)),
            position=Vector2(screen_w / 4, screen_h / 4),
            boundaries=Rect(screen_w, 0, screen_h, 0),
            physics_body=PhysicsBody(
                mass=puck_physics["mass"],
                friction=puck_physics["friction"],
                elasticity=puck_physics["elasticity"],
            ),
            color=puck_color,
        )
        settings = BouncyBallSettings(
            player, puck, width=screen_w, height=screen_h, bg_color=table_color
        )

        game = BouncyBall(settings, player, puck)

        print("Starting game...")
        game.run()
        print("Game quit")
