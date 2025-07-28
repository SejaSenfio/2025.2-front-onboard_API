from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class DjangoSettings(BaseSettings):
    SECRET_KEY: str = Field(
        alias="SECRET_KEY",
        default="django-insecure-ce+&mej)lk9sn0@cz1^lt0(wm@5-4sfe7ge$i$6hryn9!=^l2p",
    )
    DEBUG: bool = Field(alias="DEBUG", default=False)


DJANGO_SETT = DjangoSettings()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = DJANGO_SETT.SECRET_KEY
DEBUG = DJANGO_SETT.DEBUG

BACKEND_APP_VERSION: str = "0.1.0-alpha.0"
