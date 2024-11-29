from django.db import models
from uuid import uuid4
from datetime import date

from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Invitation(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre del invitado")
    message = models.TextField(verbose_name="Mensaje", blank=True, null=True)
    amount = models.IntegerField(verbose_name="Cupos")
    code = models.CharField(max_length=10, verbose_name="Código", unique=True)
    expiration_date = models.DateField(verbose_name="Fecha de expiración")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")
    is_honorary_invitation = models.BooleanField("Invitación honorífica", default=False)
    confirmation = models.OneToOneField(
        "Confirmation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Confirmación",
        related_name="invitation",
    )

    def expired(self) -> bool:
        return self.expiration_date < date.today()

    def __str__(self) -> str:
        return f"{self.name} ({self.amount})"


@receiver(post_save, sender=Invitation)
def generate_code(sender, instance, created, **kwargs):
    if created:
        instance.code = f"LYD-{str(uuid4())[:4].upper()}"
        instance.save()


class Confirmation(models.Model):
    will_attend = models.BooleanField(verbose_name="Asistirá")
    amount = models.IntegerField(verbose_name="Cantidad de asistentes")
    food_restrictions = models.TextField(verbose_name="Restricciones alimenticias")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")
