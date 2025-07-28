class SmsBaseException(BaseException):
    def __init__(self, response: dict, message: str | None = None, code: int | str | None = None):
        if not message:
            message = response.get("description", "Requisição de envio de SMS falhou.")
        if not code:
            code = response.get("code")
        self.message = message
        self.code = response.get("code")
        self.crud = response

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: code: {self.code} | message: {self.message} | crud: {self.crud}"


class SmsRequestException100(SmsBaseException):
    pass


class SmsRequestException101(SmsBaseException):
    pass


class SmsRequestException102(SmsBaseException):
    pass


class SmsRequestException103(SmsBaseException):
    pass


class SmsRequestException104(SmsBaseException):
    pass


class SmsRequestException105(SmsBaseException):
    pass


class SmsRequestException106(SmsBaseException):
    pass


class SmsRequestException107(SmsBaseException):
    pass
