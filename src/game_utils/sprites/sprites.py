
from pygame import Surface, Vector3
from pygame.sprite import Sprite


__SPRITES = {}

class GameSprite(Sprite):
    CONTROLLER_INPUT = "controller"
    DELTA_TIME = "dt"

    """_summary_

    Args:
        id (int): unique id for the sprite.  can be ordinal
        image (pygame.Surface): Surface on which to draw the sprite
        position (pygame.Vector3): Position on screen to draw the sprite
        boundaries (pygame.Rect | None): Optional boundaries in which to keep the sprite.  Defaults to None
    """
    def __init__(
        self,
        image: Surface,
        position: Vector3,
        controller=None,
        boundaries=None,
        physics_body=None
    ):
        """Implement a Game Sprite object. Subclass must implement GameSprite.update

        Args:
            image (Surface): The image for the sprite
            position (Vector3): Where to put the sprite
            controller (Controller | None, optional): The controller for the sprite
            boundaries (Rect | None, optional): Optional boundary coordinates
            physics_body (PhysicsBody | None, optional): The physics body for the sprite
        """
        super().__init__()
        self.__image = image
        self.__position = position
        self.controller = controller
        self.boundaries = boundaries
        self.physics_body = physics_body

    def update(self, position: Vector3):
        """update this sprite with given information
        """
        self.__position = position

    def get_rect(self):
        return self.__image.get_rect()
    
    def get_image(self):
        return self.__image
    
    def get_position(self):
        return self.__position


