import re
from datetime import date as dt_date
from datetime import datetime as dt_datetime
from decimal import Decimal

from django.utils import timezone
from pydantic import BaseModel as PydanticBaseModel
from pydantic import EmailStr
from pydantic import ValidationError as PydanticValidationError

from .patterns import (
    CNPJ_PATTERN,
    DATE_API_PATTERN,
    DATETIME_API_FORMAT,
    DATETIME_API_PATTERN,
    DATETIME_API_STRING_FORMAT,
    LATITUDE_PATTERN,
    LONGITUDE_PATTERN,
    MAC_ADDRESS_PATTERN,
    MAC_ADDRESS_PATTERN_API,
    MAC_ADDRESS_PATTERN_NO_COLON,
    PHONE_NUMBER_PATTERN,
    TAG_SERIAL_NUMBER,
    USER_PASSWORD_PATTERN,
)


def validate_user_password(password: str) -> str:
    """
    Valida a senha informada.

    Args:
        password: A senha a ser validada.

    Returns:
        A senha validada.

    Raises:
        ValueError: Se a senha for inválida.
    """
    if not re.match(pattern=USER_PASSWORD_PATTERN, string=str(password)):
        raise ValueError(
            "A senha deve conter no mínimo 8 caracteres, pelo menos uma letra maiúscula, uma letra minúscula e um número."
        )
    return password


def validate_mac_address(mac_address: str, autofix: bool = False, from_api: bool = False) -> str:
    """
    Valida um endereço MAC.

    Args:
        mac_address (str): O endereço MAC a ser validado.
        autofix (bool, optional): Se True, o endereço MAC será corrigido automaticamente. Padrão é False.
        from_api (bool, optional): Se True, o endereço MAC será validado sem dois pontos. Padrão é False.

    Returns:
        str: O endereço MAC validado.

    Raises:
        ValueError: Se o endereço MAC for inválido.
    """
    if from_api:
        if not re.search(MAC_ADDRESS_PATTERN_API, mac_address):
            if autofix and re.search(MAC_ADDRESS_PATTERN_NO_COLON, mac_address):
                return str(
                    ":".join(mac_address[i : i + 2] for i in range(0, len(mac_address), 2))
                ).upper()
            raise ValueError("Endereço MAC inválido")
        return mac_address.upper()

    if not re.search(MAC_ADDRESS_PATTERN, mac_address):
        if autofix and re.search(MAC_ADDRESS_PATTERN_NO_COLON, mac_address):
            return str(
                ":".join(mac_address[i : i + 2] for i in range(0, len(mac_address), 2))
            ).upper()
        raise ValueError("Endereço MAC inválido")
    return mac_address.upper()


def validate_cnpj(cnpj: str) -> str:
    """
    Valida o CNPJ informado.

    Args:
        cnpj (str): O CNPJ a ser validado.

    Returns:
        str: O CNPJ validado.

    Raises:
        ValueError: Se o CNPJ for inválido.
    """
    if not re.search(CNPJ_PATTERN, cnpj):
        raise ValueError(f"CNPJ inválido: {cnpj}. O formato esperado é XX.XXX.XXX/XXXX-XX")
    return cnpj


def validate_latitude(latitude: float | str | int | Decimal) -> float | str | int | Decimal:
    """
    Valida a latitude informada.

    Args:
        latitude (float|str|int): A latitude a ser validada.

    Returns:
        float|str|int: A latitude validada.

    Raises:
        ValueError: Se a latitude for inválida.
    """
    if not re.search(LATITUDE_PATTERN, str(latitude)):
        raise ValueError("Latitude inválida, por favor informe um valor de latitude")
    return latitude


def validate_longitude(longitude: float | str) -> float | EmailStr:
    """
    Valida a longitude informada.

    Args:
        longitude: A longitude a ser validada.

    Returns:
        A longitude validada.

    Raises:
        ValueError: Se a longitude for inválida.
    """
    if not re.search(LONGITUDE_PATTERN, str(longitude)):
        raise ValueError("Longitude inválida, por favor informe um valor de longitude")
    return longitude


def validate_datetime(datetime: str | dt_datetime, make_aware: bool = True) -> dt_datetime:
    """
    Valida o valor de data e hora.

    Args:
        datetime: O valor de data e hora a ser validado.
        make_aware: Se True, a data e hora será convertida para uma data e hora com fuso horário.

    Returns:
        O valor de data e hora validado como uma data e hora com fuso horário.

    Raises:
        ValueError: Se o valor de data e hora for inválido.
    """
    if isinstance(datetime, str):
        if not re.match(DATETIME_API_PATTERN, datetime.strip()):
            raise ValueError(
                f"Data e hora com formato inválido. Formato esperado: {DATETIME_API_STRING_FORMAT}"
            )

        dt = dt_datetime.strptime(datetime, DATETIME_API_FORMAT)

        if make_aware and timezone.is_naive(dt):
            return timezone.make_aware(dt)

        return dt
    elif isinstance(datetime, dt_datetime):
        if make_aware and timezone.is_naive(datetime):
            return timezone.make_aware(datetime)

        return datetime

    raise ValueError(f"Tipo inválido para a data e hora: {type(datetime)}")


def validate_date(date: str | dt_date) -> dt_date:
    """
    Valida o valor da data.

    Args:
        date: O valor da data a ser validado.

    Returns:
        O valor da data validado.

    Raises:
        ValueError: Se o valor da data for inválido.
    """
    if isinstance(date, dt_date):
        return date

    if not re.match(DATE_API_PATTERN, date.strip()):
        raise ValueError("Data com formato inválido. Formato esperado: YYYY-MM-DD")

    dt = dt_date.fromisoformat(date)
    return dt


def validate_non_empty_string(value: str) -> str:
    """
    Valida um valor do tipo string.

    Args:
        value: O valor a ser validado.

    Returns:
        O valor validado.

    Raises:
        ValueError: Se o valor for inválido, None ou uma string vazia. Mensagem genérica.

    """

    if value is None or not isinstance(value, str) or value.strip() == "":
        raise ValueError("String vazia ou nula.")
    return value


def validate_tag_serial_number(serial_number: str | int) -> str | int:
    """
    Valida e formata um número serial de tag.
    Esta função verifica se um número serial é válido de acordo com regras predefinidas:
    - Não pode ser zero ou vazio
    - Deve ser um valor numérico entre 1 e 9999
    - Se tiver menos que 4 dígitos, será preenchido com zeros à esquerda
    Args:
        serial_number (Union[str, int]): O número serial a ser validado, pode ser string ou inteiro
    Returns:
        Union[str, int]: O número serial validado, preenchido com zeros se necessário
    Raises:
        ValueError: Se o número serial for zero, vazio ou fora do intervalo válido (1-9999)
    Exemplo:
        >>> validate_tag_serial_number(123)
        '0123'
        >>> validate_tag_serial_number('0456')
        '0456'
    """

    if not serial_number or not int(serial_number):
        raise ValueError("Número serial inválido, zero não é aceito!")
    if not re.match(TAG_SERIAL_NUMBER, str(serial_number)):
        new_value = str(int(serial_number)).zfill(4)
        if not re.match(TAG_SERIAL_NUMBER, new_value):
            raise ValueError(
                f"O campo 'serial_number' deve ser um valor numérico entre 1 e 9999, mas o valor informado foi {serial_number}"
            )
        return new_value
    return serial_number


def validate_phone_number(phone_number: str) -> str:
    """
    Valida uma string de número de telefone contra um padrão predefinido.
    Args:
        phone_number (str): String do número de telefone a ser validada. Formato esperado: +55912345678
    Returns:
        str: O número de telefone validado se ele corresponder ao padrão
    Raises:
        ValueError: Se o número de telefone não corresponder ao formato esperado
    Exemplo:
        >>> validate_phone_number("+5581912345678")
        "+5581912345678"
        >>> validate_phone_number("123")
        ValueError: Telefone inválido! Formato esperado: +5581912345678
    """

    if not re.match(PHONE_NUMBER_PATTERN, phone_number):
        raise ValueError("Telefone inválido! Formato esperado: +5581912345678")
    return phone_number


class _EmailValidatorModel(PydanticBaseModel):
    email: EmailStr


def validate_email(email: str) -> str:
    """
    Valida se a string fornecida é um formato de email válido.
    Args:
        email (str): A string de email a ser validada.
    Returns:
        str: A string de email validada se a validação passar.
    Raises:
        ValueError: Se o formato do email for inválido, inclui a mensagem original do erro de validação.
    Exemplos:
        >>> validate_email("user@example.com")
        'user@example.com'
        >>> validate_email("invalid-email")
        ValueError: Email inválido: ...
    """

    try:
        _EmailValidatorModel(email=email)
        return email
    except PydanticValidationError as exc:
        raise ValueError(f"Email inválido: {str(exc)} ") from exc
