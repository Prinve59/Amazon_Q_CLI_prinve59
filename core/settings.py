"""
Game settings and configuration constants
"""

# Display settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 120
TITLE = "NeuroShot: Reflex Protocol"
SCALE_TO_FULLSCREEN = True  # New setting to enable proper fullscreen scaling

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
VALORANT_RED = (255, 70, 85)
VALORANT_BLUE = (18, 184, 253)

# Game settings
CROSSHAIR_SIZE = 16
TARGET_SIZE_MIN = 25
TARGET_SIZE_MAX = 50
TARGET_SPEED_MIN = 1.5
TARGET_SPEED_MAX = 4
TARGET_LIFETIME_MIN = 1500  # milliseconds
TARGET_LIFETIME_MAX = 3500  # milliseconds
TARGET_SPAWN_RATE = 1200  # milliseconds
MAX_TARGETS = 8

# Scoring
POINTS_HIT = 100
POINTS_HEADSHOT = 200
POINTS_MISS = -50
POINTS_PENALTY_TIME = 10  # points deducted per 100ms of reaction time

# Game modes
GAME_MODE_FLICK = "flick"
GAME_MODE_TRACKING = "tracking"
GAME_MODE_SWITCH = "switch"
GAME_MODE_SPIKE = "spike"

# Game states
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"
STATE_LEADERBOARD = "leaderboard"
STATE_SETTINGS = "settings"

# Difficulty levels
DIFFICULTY_EASY = "easy"
DIFFICULTY_MEDIUM = "medium"
DIFFICULTY_HARD = "hard"
DIFFICULTY_EXTREME = "extreme"

# Difficulty modifiers
DIFFICULTY_MODIFIERS = {
    DIFFICULTY_EASY: {
        "target_speed_multiplier": 0.7,
        "target_size_multiplier": 1.3,
        "target_lifetime_multiplier": 1.5,
        "spawn_rate_multiplier": 0.7
    },
    DIFFICULTY_MEDIUM: {
        "target_speed_multiplier": 1.0,
        "target_size_multiplier": 1.0,
        "target_lifetime_multiplier": 1.0,
        "spawn_rate_multiplier": 1.0
    },
    DIFFICULTY_HARD: {
        "target_speed_multiplier": 1.3,
        "target_size_multiplier": 0.8,
        "target_lifetime_multiplier": 0.7,
        "spawn_rate_multiplier": 1.3
    },
    DIFFICULTY_EXTREME: {
        "target_speed_multiplier": 1.7,
        "target_size_multiplier": 0.6,
        "target_lifetime_multiplier": 0.5,
        "spawn_rate_multiplier": 1.7
    }
}

# File paths
ASSETS_DIR = "assets"
IMAGES_DIR = f"{ASSETS_DIR}/images"
BACKGROUNDS_DIR = f"{IMAGES_DIR}/backgrounds"
EFFECTS_DIR = f"{IMAGES_DIR}/effects"
SOUNDS_DIR = f"{ASSETS_DIR}/sounds"
FONTS_DIR = f"{ASSETS_DIR}/fonts"
DATA_DIR = "data"
SCORES_FILE = f"{DATA_DIR}/scores.json"
SETTINGS_FILE = f"{DATA_DIR}/settings.json"

# Background maps for different modes
BACKGROUND_MAPS = {
    "flick": "haven.jpg",
    "tracking": "ascent.jpg",
    "switch": "bind.jpg",
    "spike": "split.jpg",
    "menu": "valorant_menu.jpg"
}

# Default settings
DEFAULT_SETTINGS = {
    "sound_enabled": True,
    "music_volume": 0.5,
    "sfx_volume": 0.7,
    "crosshair_color": VALORANT_RED,
    "crosshair_style": "default",
    "crosshair_size": CROSSHAIR_SIZE,
    "show_fps": True,
    "show_stats": True,
    "fullscreen": True,
    "mouse_sensitivity": 1.0,
    "click_threshold": 5  # pixels of movement allowed for a click to be registered as accurate
}
