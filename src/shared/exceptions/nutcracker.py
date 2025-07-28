"""
Esse módulo contém os objetos que abrem certas informações nas exceções; Como buscar a mensagem de erro dentro de uma exceção estruturada.
"""

import logging

from pydantic import ValidationError


class PydanticValidationErrorNutcracker:
    @staticmethod
    def get_exc(exception: ValidationError) -> type[Exception]:
        """
        Retorna a exceção disparada dentro de uma validação num objeto pydantic.
        Caso haja mais que uma exceção, retorna o primeiro.

        Args:
            exception (ValidationError): Exceção de validação estruturada pelo Pydantic

        Returns:
            Exception: Exceção disparada dentro do objeto, exemplo: ValueError
        """
        first_error = exception.errors()[0]
        ctx = first_error.get("ctx")
        if not ctx:
            logging.warning(f"Exceção sem contexto: {exception}")
            return Exception

        return ctx.get("error", Exception)

    @staticmethod
    def get_errors(exception: ValidationError) -> dict[str, list[str | None]]:
        """
        Retorna um dicionário com as mensagens de erro de uma exceção de validação estruturada pelo Pydantic.

        Args:
            exception (ValidationError): Exceção de validação estruturada pelo Pydantic

        Returns:
            dict[str, list[str]]: Dicionário com as mensagens de erro
        """

        errors = exception.errors()
        errors_dict = {
            str(error.get("loc", [""])[0]): [error.get("msg")]
            for error in errors
            if not error.get("ctx", False)
        }
        errors_dict["non_field_errors"] = [
            str(error.get("ctx", {}).get("error")) for error in errors if error.get("ctx", False)
        ]
        if not errors_dict["non_field_errors"]:
            del errors_dict["non_field_errors"]
        return errors_dict
