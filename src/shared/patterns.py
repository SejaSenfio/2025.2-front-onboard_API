"""
Aqui são definidos os padrões de validação de dados.

Esses padrões são utilizados em diversas partes do projeto,
    como validação de dados de entrada, validação de dados de saída
    e validação de dados de modelos.
"""

#### Auth
USER_PASSWORD_PATTERN = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@#$%^&*()_+!?.\-]{8,}$"  # nosec

#### Organization
CNPJ_PATTERN = r"^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$"

#### Geolocation
LATITUDE_PATTERN = r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$"
LONGITUDE_PATTERN = r"^[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$"

#### Tags
MAC_ADDRESS_PATTERN = r"^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$"
MAC_ADDRESS_PATTERN_NO_COLON = r"^([0-9A-Fa-f]{2}){6}$"
MAC_ADDRESS_PATTERN_API = r"^([0-9A-F]){12}$"
TAG_SERIAL_NUMBER = r"^(?!0000)[0-9]{4}$"

### Base
SENFIO_BASE_URL_PATTERN = r"(?:http[s]?://)?([^.]+)\.senfio\.com\.br"

### Phone number
PHONE_NUMBER_PATTERN = r"^\+55\d{2}9\d{8}$"

### Date and time | ISO 8601
DATETIME_API_PATTERN = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}-03:00$"
DATETIME_API_FORMAT = "%Y-%m-%dT%H:%M:%S-03:00"
DATETIME_API_FORMAT_MILLISECOND = "%Y-%m-%dT%H:%M:%S.%f%z"
DATETIME_API_FORMAT_TZ = "%Y-%m-%dT%H:%M:%S%z"
DATETIME_API_STRING_FORMAT = "YYYY-MM-DDThh:mm:ss-03:00"
DATETIME_SHOW_FORMAT = "%d/%m/%Y %H:%M:%S"
DATETIME_SHOW_PATTERN = r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}$"
DATETIME_SHOW_STRING_FORMAT = "DD/MM/YYYY HH:MM:SS"
DATETIME_REPORT_SHOW_FORMAT = "%d/%m/%Y %Hh%Mmin"

DATE_API_PATTERN = r"^\d{4}-\d{2}-\d{2}$"
DATE_API_FORMAT = "%Y-%m-%d"
DATE_API_STRING_FORMAT = "YYYY-MM-DD"
DATE_SHOW_FORMAT = "%d/%m/%Y"
DATE_SHOW_PATTERN = r"^\d{2}/\d{2}/\d{4}$"
DATE_SHOW_STRING_FORMAT = "DD/MM/YYYY"

TIME_SHOW_PATTERN = r"^\d{2}:\d{2}:\d{2}$"
TIME_SHOW_FORMAT = "%H:%M:%S"
TIME_SHOW_STRING_FORMAT = "HH:MM:SS"
TIME_REPORT_SHOW_FORMAT = "%Hh%Mmin"
