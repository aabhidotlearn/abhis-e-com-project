from .models.customer import Customer


def store_context(request):
    customer = None
    customer_id = request.session.get("customer_id")
    if customer_id:
        customer = Customer.objects.filter(pk=customer_id).first()

    cart_count = 0
    for quantity in request.session.get("cart", {}).values():
        try:
            cart_count += max(int(quantity), 0)
        except (TypeError, ValueError):
            continue
    return {"current_customer": customer, "cart_count": cart_count}
