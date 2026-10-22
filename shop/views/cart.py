from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from shop.models.product import Product


def get_cart_items(request):
    cart = request.session.get("cart", {})
    products = Product.objects.filter(id__in=cart.keys())
    items = []
    for product in products:
        try:
            quantity = int(cart.get(str(product.pk), 0))
        except (TypeError, ValueError):
            quantity = 0
        if quantity > 0:
            items.append({
                "product": product,
                "quantity": quantity,
                "line_total": product.price * quantity,
            })
    return items


def cart(request):
    items = get_cart_items(request)
    total = sum(item["line_total"] for item in items)
    return render(request, "cart.html", {"items": items, "total": total})


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 0
    if quantity < 1 or quantity > 99:
        messages.error(request, "Choose a quantity from 1 to 99.")
        return redirect("product_detail", product_id=product.pk)

    cart_data = request.session.get("cart", {})
    key = str(product.pk)
    cart_data[key] = min(int(cart_data.get(key, 0)) + quantity, 99)
    request.session["cart"] = cart_data
    messages.success(request, f"{product.name} was added to your cart.")
    return redirect("cart")


@require_POST
def update_cart(request):
    cart_data = request.session.get("cart", {})
    for key in list(cart_data):
        try:
            quantity = int(request.POST.get(f"quantity_{key}", cart_data[key]))
        except (TypeError, ValueError):
            quantity = 0
        if quantity <= 0:
            cart_data.pop(key, None)
        else:
            cart_data[key] = min(quantity, 99)
    request.session["cart"] = cart_data
    messages.success(request, "Your cart was updated.")
    return redirect("cart")


@require_POST
def remove_from_cart(request, product_id):
    cart_data = request.session.get("cart", {})
    cart_data.pop(str(product_id), None)
    request.session["cart"] = cart_data
    messages.success(request, "Item removed from your cart.")
    return redirect("cart")
