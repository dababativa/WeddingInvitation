# Generated by Django 5.1.2 on 2025-01-19 15:58
from datetime import timedelta
from django.db import migrations


def add_one_day_to_expiration_date(apps, schema_editor):
    Invitation = apps.get_model("invitations", "Invitation")
    invitations = Invitation.objects.all()
    for invitation in invitations:
        invitation.expiration_date = invitation.expiration_date + timedelta(days=1)
        invitation.save()


def remove_one_day_to_expiration_date(apps, schema_editor):
    Invitation = apps.get_model("invitations", "Invitation")
    invitations = Invitation.objects.all()
    for invitation in invitations:
        invitation.expiration_date = invitation.expiration_date - timedelta(days=1)
        invitation.save()


class Migration(migrations.Migration):
    dependencies = [
        ("invitations", "0002_alter_invitation_confirmation"),
    ]

    operations = [
        migrations.RunPython(
            code=add_one_day_to_expiration_date,
            reverse_code=remove_one_day_to_expiration_date,
        )
    ]
