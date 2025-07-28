from pydantic import Field
from pydantic_settings import BaseSettings


#### Database Settings
class DatabaseSettings(BaseSettings):
    DB_NAME: str = Field(alias="DB_NAME", default="postgres")
    DB_USER: str = Field(alias="DB_USER", default="postgres")
    DB_PASSWORD: str = Field(alias="DB_PASSWORD", default="postgres")
    DB_HOST: str = Field(alias="DB_HOST", default="localhost")
    DB_PORT: int = Field(alias="DB_PORT", default=5432)


DATABASE_SETT = DatabaseSettings()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": DATABASE_SETT.DB_NAME,
        "USER": DATABASE_SETT.DB_USER,
        "PASSWORD": DATABASE_SETT.DB_PASSWORD,
        "HOST": DATABASE_SETT.DB_HOST,
        "PORT": DATABASE_SETT.DB_PORT,
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
