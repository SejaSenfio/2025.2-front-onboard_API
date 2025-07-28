from pydantic import Field
from pydantic_settings import BaseSettings


class SmsSettings(BaseSettings):
    SMS_API_URL: str = Field(default="https://<API_URL>")
    SMS_API_KEY: str = Field(default="API_KEY_CHANGEME")
    SMS_TIMEOUT: int = Field(default=10)
    SMS_DEBUG_SERVICE: bool = Field(default=True)
    SMS_DEBUG_SERVICE_HOST: str = Field(default="sms_sender")
    SMS_DEBUG_SERVICE_PORT: int = Field(default=80)


SMS_SETTINGS = SmsSettings()
