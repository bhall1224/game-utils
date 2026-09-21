
from pygame import display
from pygame import FULLSCREEN, Color, Surface, Vector2

ColorType = str | tuple[int, int, int] | Color

class ScreenSettings:
    def __init__ (
        self,
        dimensions: Vector2 | None = None,
        title: str | None = None,
        bg_color: ColorType | None = None,
        bg_image: Surface | None = None,
    ):
        if dimensions is None:
            self.__screen_surface = display.set_mode((0, 0), FULLSCREEN)
            self.__dimensions = Vector2(
                self.__screen_surface.get_width(),
                self.__screen_surface.get_height()
            )
        else:
            self.__dimensions = dimensions
            self.__screen_surface = display.set_mode(self.__dimensions)

        if title is not None:
            display.set_caption(title)
        
        self.__bg_color = bg_color
        self.__bg_image = bg_image

    def update_screen(self):
        if self.__bg_color is not None:
            self.__screen_surface.fill(self.__bg_color)
        elif self.__bg_image is not None:
            self.__screen_surface.blit(self.__bg_image, self.__dimensions)
        display.flip()

    def draw_image(self, image):
        self.__screen_surface.blit(image, image.get_rect())

    def get_dimensions(self):
        return self.__dimensions
    
    def get_screen(self):
        return self.__screen_surface