from pathlib import Path

from .base import BASE_DIR

MEDIA_ROOT = Path.joinpath(BASE_DIR, "media")
MEDIA_URL = "/media/"
