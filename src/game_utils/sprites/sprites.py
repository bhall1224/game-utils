from collections.abc import Callable

from pygame import Surface, Vector2
from pygame.sprite import Sprite

from game_utils.physics.physics import PhysicsBody

#####################################################################################
# Type aliases for callback function types
#####################################################################################

CallbackType = Callable[[float, Vector2], None]

#####################################################################################
# Class for registering and injecting sprites
#####################################################################################

class Sprites:
    def __init__(self):
        self.__sprites: dict[str, GameSprite] = {}

    def add(self, name):
        def __inner(fn):
            self.__sprites[name] = fn()
        return __inner

    def sprites(self):
        def __inner(fn):
            def __event_wrapper(event, settings, config):
                return fn(event, self.__sprites, settings, config)
            return __event_wrapper
        return __inner

#####################################################################################
# Class for Pygame Sprite behaviors
#####################################################################################

class GameSprite(Sprite):
    """A class for game sprite behaviors"""

    def __init__(
        self,
        image: Surface,
        position: Vector2,
        physics_body: PhysicsBody = None,
        update_callbacks: list[Callable[[Vector2], Vector2]] = []
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
        self.__image = image
        self.__position = position
        self.__physics_body = physics_body
        self.__update_callbacks = update_callbacks

    def update(self, *args, **kwargs):
        """update the sprite's position.  If a physics body is given, will automatically bind to its position

        Args:
            position (Vector2): a new position for this sprite. Defaults to None
            config: the given configurations for this game
        """
        # if given, bind to the physics body position
        if self.__physics_body is not None:
            self.__position = self.__physics_body.position

        # make no change if not given
        position: Vector2 = Vector2(0.0, 0.0)  
        if len(args) > 0:
            position = args[0]
        elif len(kwargs) > 0:
            position = kwargs.pop("position", position)

        self.__position += position

        # Any other behaviors to bind to this sprite
        for callback in self.__update_callbacks:
            self.__position += callback(self.__position)

    def get_rect(self):
        return self.__image.get_rect()

    def get_image(self):
        return self.__image

    def get_position(self):
        return self.__position
