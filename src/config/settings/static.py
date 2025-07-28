from pathlib import Path

from .base import BASE_DIR

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATIC_ROOT = Path.joinpath(BASE_DIR, "../infra/nginx/static")
