from django.contrib import admin
from django.http import HttpRequest
from .models import Invitation, Confirmation
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Confirmation, Invitation
# Register your models here.

class ConfirmationResource(resources.ModelResource):
    guest = fields.Field(
        column_name='guest',
        attribute='invitation__name',
    )

    class Meta:
        model = Confirmation
        fields = ('id', 'guest', 'will_attend', 'food_restrictions')
        export_order = ('id', 'guest', 'will_attend', 'food_restrictions')


class InvitationAdmin(ImportExportModelAdmin):
    model = Invitation
    list_display = ["name", "amount", "code"]


class ConfirmationAdmin(ImportExportModelAdmin):
    model = Confirmation
    resource_class = ConfirmationResource
    list_display = ["invitation", "will_attend", "has_food_restrictions"]

    def has_change_permission(self, *args, **kwargs) -> bool:
        return False

    def has_add_permission(self, *args, **kwargs) -> bool:
        return False

    def has_delete_permission(self, *args, **kwargs) -> bool:
        return False

    def has_food_restrictions(self, obj):
        return "Si" if bool(obj.food_restrictions) else "No"


admin.site.register(Confirmation, ConfirmationAdmin)
admin.site.register(Invitation, InvitationAdmin)
