from collections.abc import Callable

from pygame import Surface, Vector2
from pygame.sprite import Sprite

from game_utils.controller.controller import Controller
from game_utils.physics.physics import PhysicsBody

CallbackType = Callable[[float, Vector2], None]


class GameSprite(Sprite):
    """A class for game sprite behaviors"""

    def __init__(
        self,
        image: Surface,
        position: Vector2,
        controller: Controller = None,
        physics_body: PhysicsBody = None,
        boundaries: Vector2 = None,
    ):
        """Create a new instance of GameSprite

        Args:
            image (Surface): The image for the sprite
            position (Vector2): Where to put the sprite
            controller (Controller | None, optional): The controller for the sprite
            boundaries (Rect | None, optional): Optional boundary coordinates
            physics_body (PhysicsBody | None, optional): The physics body for the sprite
        """
        super().__init__()
        self._image = image
        self._position = position
        self._controller = controller
        self._boundaries = boundaries
        self._physics_body = physics_body
        self._update_callbacks = []

    def update(self, *args, **kwargs):
        """update the sprite's position

        Args:
            dt (float): the change in time.  Defaults to None
            position (Vector2): a new position for this sprite. Defaults to None
            **config: the given configurations for this game
        """
        dt: float = 1.0  # make no change if not given
        position: Vector2 = Vector2(0.0, 0.0)  # make no change if not given
        config = {}
        if len(args) > 0:
            dt = args[0]
            position = args[1] if len(args) > 1 else position
        elif len(kwargs) > 0:
            dt = kwargs.pop("dt")
            position = kwargs.pop("position", position)
            config = kwargs

        self._position += position * dt

        for callback in self._update_callbacks:
            callback(dt, position**config)

    def get_rect(self):
        return self.__image.get_rect()

    def get_image(self):
        return self.__image

    def get_position(self):
        return self.__position

    def update_callback(self, name=None):
        def __inner(fn):
            self.__update_callbacks.append(fn)
