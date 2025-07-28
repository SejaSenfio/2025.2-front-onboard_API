from rest_framework.exceptions import ValidationError
from rest_framework.request import Request


def deactivate_validator_for_patch(request: Request, *args: list, **kwargs: dict) -> None:
    """
    Valida se o campo 'deactivated' está presente no request.data e se é o único campo presente.
    Usado para as views que desativam/ativam um objeto.
    """
    if "deactivated" not in request.data:
        raise ValidationError({"deactivated": ["Este campo é obrigatório."]})

    if len(request.data) > 1:
        raise ValidationError(
            {"deactivated": ["Apenas o campo 'deactivated' pode ser atualizado através do patch."]}
        )
