from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views import View

from shop.models.customer import Customer

class signup(View):
    def get(self, request):
        return render(request, "signup.html")

    def post(self, request):
        values = {
            "fn": request.POST.get("fn", "").strip(),
            "ln": request.POST.get("ln", "").strip(),
            "email": request.POST.get("email", "").strip().lower(),
            "mobile": request.POST.get("mobile", "").strip(),
        }
        password = request.POST.get("password", "")

        error = None
        if not values["fn"]:
            error = "First name is required."
        elif not values["ln"]:
            error = "Last name is required."
        elif not values["email"]:
            error = "Email address is required."
        else:
            try:
                validate_email(values["email"])
            except ValidationError:
                error = "Enter a valid email address."
        if error is None and Customer.objects.filter(email__iexact=values["email"]).exists():
            error = "An account with this email address already exists. Please use a different email."
        elif error is None and (not values["mobile"].isdigit() or len(values["mobile"]) != 10):
            error = "Enter a 10-digit mobile number."
        elif error is None and len(password) < 8:
            error = "Password must contain at least 8 characters."

        if error:
            return render(request, "signup.html", {"error": error, "value": values})

        Customer.objects.create(
            first_name=values["fn"],
            last_name=values["ln"],
            email=values["email"],
            mobile=values["mobile"],
            password=make_password(password),
        )
        return render(request, "signup.html", {
            "success": "Account created successfully. You can now log in.",
        })
