from django.db import models
from uuid import uuid4
from datetime import date


# Create your models here.
class Invitation(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre del invitado")
    message = models.TextField(verbose_name="Mensaje", blank=True, null=True)
    amount = models.IntegerField(verbose_name="Cupos")
    code = models.UUIDField(default=uuid4, editable=False)
    expiration_date = models.DateField(verbose_name="Fecha de expiración")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")
    is_honorary_invitation = models.BooleanField("Invitación honorífica", default=False)
    confirmation = models.OneToOneField(
        "Confirmation",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Confirmación",
        related_name="invitation",
    )

    def expired(self) -> bool:
        return self.expiration_date < date.today()

    def __str__(self) -> str:
        return f"{self.name} ({self.amount})"


class Confirmation(models.Model):
    will_attend = models.BooleanField(verbose_name="Asistirá")
    amount = models.IntegerField(verbose_name="Cantidad de asistentes")
    food_restrictions = models.TextField(verbose_name="Restricciones alimenticias")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")
