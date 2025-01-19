from django.contrib import admin
from .models import Invitation, Confirmation
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from .models import Confirmation, Invitation
from datetime import date, timedelta, datetime

# Register your models here.


class ConfirmationResource(resources.ModelResource):
    guest = fields.Field(
        column_name="guest",
        attribute="invitation__name",
    )

    class Meta:
        model = Confirmation
        fields = ("id", "guest", "will_attend", "amount", "food_restrictions")
        export_order = ("id", "guest", "will_attend", "amount", "food_restrictions")


class ExpiredFilter(admin.SimpleListFilter):
    title = "Expiró"
    parameter_name = "expired"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Si"),
            ("no", "No"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(expiration_date__lt=date.today())
        if self.value() == "no":
            return queryset.filter(expiration_date__gte=date.today())
        return queryset


class InvitationAdmin(ImportExportModelAdmin):
    model = Invitation
    list_display = ["name", "amount", "code", "expired", "expiration_date"]
    readonly_fields = ["code"]
    search_fields = ["name", "code"]
    list_filter = ["is_honorary_invitation", ExpiredFilter]

    def expired(self, obj):
        utc_expiration_date = datetime.combine(
            obj.expiration_date, datetime.min.time()
        ) + timedelta(hours=5)
        print(
            "Expiration date: ",
            utc_expiration_date,
            "-",
            "Current time: ",
            datetime.today(),
        )
        return utc_expiration_date < datetime.today()

    expired.boolean = True


class ConfirmationAdmin(ImportExportModelAdmin):
    model = Confirmation
    resource_class = ConfirmationResource
    list_display = ["invitation", "will_attend", "amount", "has_food_restrictions"]
    search_fields = ["invitation__name", "invitation__code"]
    list_filter = ["will_attend"]

    def has_change_permission(self, *args, **kwargs) -> bool:
        return False

    def has_add_permission(self, *args, **kwargs) -> bool:
        return False

    def has_food_restrictions(self, obj):
        return "Si" if bool(obj.food_restrictions) else "No"


admin.site.register(Confirmation, ConfirmationAdmin)
admin.site.register(Invitation, InvitationAdmin)
