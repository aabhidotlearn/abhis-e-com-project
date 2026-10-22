from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from shop.models.customer import Customer
from shop.models.order import Order, OrderItem
from shop.models.product import Product
from .cart import get_cart_items


def current_customer(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return None
    return Customer.objects.filter(pk=customer_id).first()


@require_http_methods(["GET", "POST"])
def checkout(request):
    customer = current_customer(request)
    if customer is None:
        next_url = reverse("checkout")
        return redirect(f"{reverse('login')}?next={next_url}")

    items = get_cart_items(request)
    if not items:
        messages.info(request, "Your cart is empty. Add a product before checkout.")
        return redirect("cart")

    total = sum((Decimal(item["line_total"]) for item in items), Decimal("0.00"))
    if request.method == "GET":
        return render(request, "checkout.html", {"items": items, "total": total})

    shipping_address = request.POST.get("shipping_address", "").strip()
    if not shipping_address:
        return render(request, "checkout.html", {
            "items": items,
            "total": total,
            "shipping_address": shipping_address,
            "error": "Enter a shipping address to place your order.",
        })

    with transaction.atomic():
        order = Order.objects.create(
            customer=customer,
            shipping_address=shipping_address,
            total=total,
        )
        OrderItem.objects.bulk_create([
            OrderItem(
                order=order,
                product=item["product"],
                product_name=item["product"].name,
                unit_price=item["product"].price,
                quantity=item["quantity"],
            )
            for item in items
        ])

    request.session["cart"] = {}
    return redirect("order_detail", order_id=order.pk)


def order_detail(request, order_id):
    customer = current_customer(request)
    if customer is None:
        next_url = reverse("order_detail", kwargs={"order_id": order_id})
        return redirect(f"{reverse('login')}?next={next_url}")
    order = get_object_or_404(Order, pk=order_id, customer=customer)
    return render(request, "order_detail.html", {"order": order})


def order_list(request):
    customer = current_customer(request)
    if customer is None:
        return redirect(f"{reverse('login')}?next={reverse('orders')}")
    orders = Order.objects.filter(customer=customer).prefetch_related("items")
    return render(request, "orders.html", {"orders": orders})
