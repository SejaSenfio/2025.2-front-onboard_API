from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field


class WhatsappSettings(PydanticBaseModel):
    WHATSAPP_API_USER: str = Field(default="USER_CHANGEME")
    WHATSAPP_API_PASS: str = Field(default="PASS_CHANGEME")
    WHATSAPP_API_KEY: str = Field(default="API_KEY_CHANGEME")
    WHATSAPP_API_SID: str = Field(default="API_SID_CHANGEME")
    WHATSAPP_API_URL: str = Field(default=f"https://<API_URL>/{WHATSAPP_API_SID}/sendMessage")
    WHATSAPP_TIMEOUT: int = Field(default=10)
    WHATSAPP_DEBUG_SERVICE: bool = Field(default=True)
    WHATSAPP_DEBUG_SERVICE_HOST: str = Field(default="whatsapp_sender")
    WHATSAPP_DEBUG_SERVICE_PORT: int = Field(default=80)


WHATSAPP_SETTINGS = WhatsappSettings()
