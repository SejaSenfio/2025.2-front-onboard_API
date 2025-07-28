from pydantic import Field
from pydantic_settings import BaseSettings


class EmailSettings(BaseSettings):
    EMAIL_API_KEY: str = Field(default="<API_KEY>")
    EMAIL_SENFIO_FROM: str = Field(default="naoresponda@senfio.com.br")
    EMAIL_SENFIO_REPLY_TO: str = Field(default="suporte@senfio.com.br")
    EMAIL_API_URL: str = Field(default="https://api.sendgrid.com/v3/mail/send")
    EMAIL_REQ_TIMEOUT: int = Field(default=5)
    EMAIL_LOCAL_SERVICE: bool = Field(default=True)
    ##-----------Dev Mail Service-----------------##
    DEV_MAIL_HOST: str = Field(default="dev-mail")
    DEV_MAIL_PORT: int = Field(default=1025)
    DEV_MAIL_USER: str = Field(default="")
    DEV_MAIL_PASS: str = Field(default="")
    ##----------------------------------------------##


EMAIL_SETTINGS = EmailSettings()
# -------------------------------------------------------------------#

# Dev Mail service
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = EMAIL_SETTINGS.DEV_MAIL_HOST
EMAIL_PORT = EMAIL_SETTINGS.DEV_MAIL_PORT
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
EMAIL_HOST_USER = EMAIL_SETTINGS.DEV_MAIL_USER
EMAIL_HOST_PASSWORD = EMAIL_SETTINGS.DEV_MAIL_PASS
DEFAULT_FROM_EMAIL = "dev.app.senfio@senfio.com"
