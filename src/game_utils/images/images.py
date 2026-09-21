from pygame import Rect, Surface


class __SpriteSheet:
    """Allows user to access segements of a sprite sheet"""

    def __init__(
        self,
        spritesheet: Surface,
        n_sprites: int = 1,
        n_lists: int = 1,
        bg_color: str | None = None,
    ) -> None:
        self.__spritesheet = spritesheet
        self.__bg_color = bg_color
        self.__n_lists = n_lists
        self.__n_sprites = n_sprites
        self.__sprite_size = Rect((0, 0), (self.rect.height, self.rect.width / n_sprites))
        self.__sprite_rects = [
            # add a new rectangle for n sprites in this sheet (by m lists)
            Rect(
                (self.__sprite_size.x + i * self.__sprite_size.w, self.__sprite_size.y),
                self.__sprite_size.size,
            )
            for i in range(self.__n_sprites)
            for _ in range(self.__n_lists)
        ]

    def _get_spritesheet_segment(self, rect: Rect) -> Surface:
        """Get a segment of the spritesheet using the given coordinates

        Args:
            rect (Rect): The coordinates of the segment you want me to find in the spritesheet

        Returns:
            Surface: The sprite from the spritesheet using the given coordinates
        """
        image = Surface(rect.size)
        if self.__bg_color is not None:
            image.fill(self.__bg_color)
        image.blit(self.__spritesheet, (0, 0), rect)
        return image
    
    def _get_sprite_rects(self) -> list[Rect]:
        return self.__sprite_rects


class SpriteSheetList(__SpriteSheet):
    """implements sprite sheet as a list of sprites.  sprites are indexed"""
    def __init__(self, spritesheet, n_sprites = 1, n_lists = 1, bg_color = None):
        super().__init__(spritesheet, n_sprites, n_lists, bg_color)

    def __getitem__(self, index: int) -> Surface:
        if index >= len(self._get_sprite_rects()):
            msg = f"index {index} out of bounds"
            raise IndexError(msg)

        return self._get_spritesheet_segment(self._get_sprite_rects()[index])


class SpriteSheetMap(__SpriteSheet):
    """Implements a sprite sheet as a dictionary of sprites"""

    def __init__(
        self,
        spritesheet: Surface,
        keys: list[str] = ["0"],
        n_sprites: int = 1,
        n_lists: int = 1,
        bg_color: str | None = None,
    ) -> None:
        super().__init__(spritesheet, n_sprites, n_lists, bg_color)
        if len(keys) < len(self._get_sprite_rects()):
            raise Exception("Not enough keys for sprites determined")

        self.__keys = keys
        self.__sprite_map = {
            self.__keys[i]: self._get_sprite_rects()[i] for i in range(len(self.__keys))
        }

    def get(self, name) -> Surface | None:
        s = self.__sprite_map.get(name)

        if s is not None:
            return self._get_spritesheet_segment(s)

    def __getitem__(self, name: str) -> Surface | None:
        s = self.__sprite_map.get(name)

        if s is None:
            msg = f"No key {name}"
            raise KeyError(msg)

        return self._get_spritesheet_segment(s)
