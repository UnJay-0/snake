from dataclasses import dataclass, fields, asdict, field
import json, pygame
from pathlib import Path
from src.utils import UP, DOWN, LEFT, RIGHT, CONFIRM, Command

SETTINGS_PATH = Path(__file__).parent.parent / 'config' / 'settings.json'
GRAPHICS_PATH = Path("assets/graphics")
FONTS_PATH = Path("assets/fonts")

@dataclass
class Keybindings:
    player_1: dict[int, Command] = field(default_factory=lambda:{
        pygame.K_w: UP,
        pygame.K_s: DOWN,
        pygame.K_a: LEFT,
        pygame.K_d: RIGHT
    })
    player_2: dict[int, Command] = field(default_factory=lambda:{
        pygame.K_UP: UP,
        pygame.K_DOWN: DOWN
    })
    ui_movement: dict[int, Command] = field(default_factory=lambda:{
        pygame.K_UP: UP,
        pygame.K_DOWN: DOWN,
        pygame.K_LEFT: LEFT,
        pygame.K_RIGHT: RIGHT,
        pygame.K_KP_ENTER: CONFIRM
    })

@dataclass
class AppSettings:
    frame_rate: int = 60
    resolution: tuple[int] = (800, 500)
    field_dimensions: tuple[list[int]] = ([0, 800], [100, 500])
    fullscreen: bool = False
    music_volume: float = 0.6
    sfx_volume: float = 0.8
    keybindings: Keybindings = field(default_factory=Keybindings)

    def __post_init__(self):
            if isinstance(self.keybindings, dict):
                self.keybindings = Keybindings(**self.keybindings)

    @classmethod
    def load_settings(cls) -> "AppSettings":
        """
        Loads the settings.
        If the settings file does not exists or does not contain specific keys
        those will be overwritten by the default settings.

        Returns
        -------
        dict
            settings for the game and application.
        """
        SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
        if SETTINGS_PATH.exists():
            with SETTINGS_PATH.open("r", encoding="utf-8") as f:
                data = json.load(f)
            valid_keys = {f.name for f in fields(cls)}
            return cls(**{k: v for k, v in data.items() if k in valid_keys})
        else:
            app_settings = cls()
            save_settings(asdict(app_settings))
            return app_settings

def save_settings(settings: dict):
    """
    Save the settings given.

    Parameters
    ----------
    settings: dict
        settings to be saved
    """
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SETTINGS_PATH.open("w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)
