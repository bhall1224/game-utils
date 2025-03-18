from pygame import Rect, Surface


class SpriteSheet:
    """Allows user to access segements of a sprite sheet"""

    def __init__(self, spritesheet: Surface, bg_color: str | None = None) -> None:
        self.spritesheet = spritesheet
        self.rect = self.spritesheet.get_rect()
        self.bg_color = bg_color

    def get_spritesheet_segment(self, rect: Rect) -> Surface:
        """Get a segment of the spritesheet using the given coordinates

        Args:
            rect (Rect): The coordinates of the segment you want me to find in the spritesheet

        Returns:
            Surface: The sprite from the spritesheet using the given coordinates
        """
        image = Surface(rect.size)
        if self.bg_color is not None:
            image.fill(self.bg_color)
        image.blit(self.spritesheet, (0, 0), rect)
        return image


class SpriteSheetList(SpriteSheet):
    """implements sprite sheet as a list of sprites.  sprites are indexed"""

    def __init__(
        self,
        spritesheet: Surface,
        n_sprites: int = 1,
        n_lists: int = 1,
        bg_color: str | None = None,
    ) -> None:
        super().__init__(spritesheet, bg_color)
        self.n_sprites = n_sprites
        self.sprite_size = Rect((0, 0), (self.rect.height, self.rect.width / n_sprites))
        self.sprite_rects = [
            # add a new rectangle for n sprites in this sheet (by m lists)
            Rect(
                (self.sprite_size.x + i * self.sprite_size.w, self.sprite_size.y),
                self.sprite_size.size,
            )
            for i in range(self.n_sprites)
            for _ in range(n_lists)
        ]

    def __getitem__(self, index: int) -> Surface:
        if index >= len(self.sprite_rects):
            msg = f"index {index} out of bounds"
            raise IndexError(msg)

        return self.get_spritesheet_segment(self.sprite_rects[index])


class SpriteSheetMap(SpriteSheetList):
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
        if len(keys) < len(self.sprite_rects):
            raise Exception("Not enough keys for sprites determined")

        self.keys = keys
        self.sprite_map = {
            self.keys[i]: self.sprite_rects[i] for i in range(len(self.keys))
        }

    def get(self, name) -> Surface | None:
        s = self.sprite_map.get(name)

        if s is not None:
            return self.get_spritesheet_segment(s)

    def __getattribute__(self, name: str) -> Surface | None:
        s = self.sprite_map.get(name)

        if s is None:
            msg = f"No key {name}"
            raise KeyError(msg)

        return self.get_spritesheet_segment(s)
