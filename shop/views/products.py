from django.shortcuts import get_object_or_404, render

from shop.models.product import Product


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "product.html", {"product": product})
