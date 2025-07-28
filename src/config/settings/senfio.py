from pydantic import Field
from pydantic_settings import BaseSettings


class SenfioSettings(BaseSettings):
    MY_SENFIO_URL: str = Field(default="https://dummy-dev.senfio.com.br")


SENFIO_SETT = SenfioSettings()
