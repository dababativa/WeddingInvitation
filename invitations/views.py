from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

# Create your views here.
from django.http import HttpResponse
from .models import Invitation, Confirmation
from django.views.decorators.csrf import csrf_exempt


def parse_checkbox(value: str) -> bool:
    return value == "on"


def index(request):
    return render(request, "invitations/index.html")


@csrf_exempt
def process_invitation_code(request):
    if request.method == "POST":
        invitation_code = request.POST.get("invitation_code")
        invitation_code = invitation_code.strip()
        return redirect(reverse("invitation_detail", args=[invitation_code]))
    return redirect(reverse("index"))


class DetailView(generic.DetailView):
    model = Invitation
    slug_field = "code"
    slug_url_kwarg = "code"
    template_name = "invitations/detail.html"

    def get_object(self, queryset=None):
        code = self.kwargs.get("code")
        try:
            return Invitation.objects.get(code=code)
        except Exception:
            return None


def confirm_invitation(request, invitation_id: int) -> HttpResponse:
    body: dict = request.POST
    confirmation = Confirmation.objects.create(
        will_attend=parse_checkbox(body.get("will_attend", "off")),
        food_restrictions=body.get("food_restrictions", ""),
        amount=body.get("amount", 0) if body.get("amount") else 0,
    )
    invitation = Invitation.objects.get(id=invitation_id)
    invitation.confirmation = confirmation
    invitation.save()
    return redirect(reverse("confirmation", args=[invitation.code]))


def confirmation(request, invitation_code: str):
    return render(
        request, "invitations/confirmation.html", {"invitation_code": invitation_code}
    )
