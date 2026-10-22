from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.views import View

from shop.models.customer import Customer

class login(View):
    def get(self,request):
        return render(request, 'login.html', {"next": request.GET.get("next", "")})

    def post(self,request):
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        customer = Customer.getemail(email)

        if customer is None:
            error = "No account was found with this email. Please sign up first."
        elif not check_password(password, customer.password):
            error = "The password is incorrect. Please try again."
        else:
            request.session.cycle_key()
            request.session["customer_id"] = customer.pk
            next_url = request.POST.get("next", "")
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect("home")

        return render(request, 'login.html', {
            'error': error,
            'email': email,
            'next': request.POST.get("next", ""),
        })


@require_POST
def logout(request):
    request.session.flush()
    return redirect("home")
