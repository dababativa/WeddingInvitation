from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "process_invitation_code/",
        views.process_invitation_code,
        name="process_invitation_code",
    ),
    path(
        "confirm_invitation/<int:invitation_id>/",
        views.confirm_invitation,
        name="confirm_invitation",
    ),
    path("<str:code>/", views.DetailView.as_view(), name="invitation_detail"),
]
