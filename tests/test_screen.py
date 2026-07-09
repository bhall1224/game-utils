from pygame import FULLSCREEN

from game_utils import screen as screen_module


class FakeSurface:
    def __init__(self, size=(0, 0)):
        self.size = size
        self.filled = []
        self.blitted = []

    def get_width(self):
        return self.size[0]

    def get_height(self):
        return self.size[1]

    def fill(self, color):
        self.filled.append(color)

    def blit(self, image, position):
        self.blitted.append((image, position))


class FakeDisplay:
    def __init__(self, size=(800, 600)):
        self.size = size
        self.surface = FakeSurface(size)
        self.modes = []
        self.captions = []
        self.flips = 0

    def set_mode(self, size=(0,0), flags=0):
        self.modes.append((size, flags))
        self.surface = FakeSurface(
            self.size if size == (0, 0) else size
        )
        return self.surface

    def set_caption(self, title):
        self.captions.append(title)

    def flip(self):
        self.flips += 1


def test_screen_settings_uses_fullscreen_when_dimensions_are_omitted():
    display_mod = FakeDisplay()

    settings = screen_module.ScreenSettings(display_mod=display_mod)

    assert settings.width == 800
    assert settings.height == 600
    assert settings.bg_color is None
    assert settings.bg_image is None
    assert display_mod.modes == [((0, 0), FULLSCREEN)]
    assert display_mod.captions == []


def test_screen_settings_uses_explicit_dimensions_and_title():
    display_mod = FakeDisplay()

    settings = screen_module.ScreenSettings(
        width=640,
        height=480,
        title="Demo",
        bg_color=(10, 20, 30),
        display_mod=display_mod,
    )

    assert settings.width == 640
    assert settings.height == 480
    assert settings.bg_color == (10, 20, 30)
    assert settings.bg_image is None
    assert display_mod.modes == [((640, 480), 0)]
    assert display_mod.captions == ["Demo"]


def test_screen_update_fills_background_and_calls_handler():
    display_mod = FakeDisplay((320, 240))

    @screen_module.screen_settings("color-screen")
    def build_settings():
        return screen_module.ScreenSettings(
            width=320,
            height=240,
            bg_color=(255, 0, 0),
            display_mod=display_mod,
        )

    @screen_module.screen_update("color-screen")
    def update(data, settings, **config):
        assert data == {"value": 1}
        assert settings.bg_color == (255, 0, 0)
        assert config["name"] == "demo"
        return {"updated": True}

    result = update({"value": 1}, name="demo")

    assert result == {"updated": True}
    assert display_mod.surface.filled == [(255, 0, 0)]
    assert display_mod.flips == 1


def test_screen_update_blits_background_image_when_color_is_missing():
    display_mod = FakeDisplay((128, 128))
    image = object()

    @screen_module.screen_settings("image-screen")
    def build_settings():
        return screen_module.ScreenSettings(
            width=128,
            height=128,
            bg_image=image,
            display_mod=display_mod,
        )

    @screen_module.screen_update("image-screen")
    def update(data, settings, **config):
        assert config == {}
        assert settings.bg_image is image
        return data

    result = update({"value": 2})

    assert result == {"value": 2}
    assert display_mod.surface.blitted == [(image, (128, 128))]
    assert display_mod.surface.filled == []
    assert display_mod.flips == 1

