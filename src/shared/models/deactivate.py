from typing import Self

from django.db import models
from model_utils.fields import MonitorField

from shared.models.validators import make_aware_if_exists


class DeactivateModel(models.Model):
    """
    Abstract deactivate model, for assurance more quality for system.
        Attributes:\n
        - deactivated
        - deactivated_at
    """

    deactivated = models.BooleanField(default=False, verbose_name="Desativado")
    deactivated_at = MonitorField(
        verbose_name="Desativado em",
        monitor="deactivated",
        when=[True],
        null=True,
        default=None,
        blank=True,
    )

    def clean(self) -> None:
        """
        Method to validate the model.
        """
        self.deactivated_at = make_aware_if_exists(self.deactivated_at)
        return super(DeactivateModel, self).clean()

    def save(self, *args: list, **kwargs: dict) -> Self:
        """
        Method to save the model.
        """
        self.clean()
        return super(DeactivateModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
