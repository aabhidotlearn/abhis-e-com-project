from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_GET

from shop.models.category import Category
from shop.models.product import Product


def serialize_product(request, product):
    return {
        'id': product.pk,
        'name': product.name,
        'description': product.desc,
        'price': product.price,
        'category': {
            'id': product.category_id,
            'name': product.category.name,
        },
        'image_url': request.build_absolute_uri(product.image.url) if product.image else None,
        'detail_url': reverse('product_detail', args=[product.pk]),
    }


@require_GET
def api_categories(request):
    categories = Category.objects.order_by('name').values('id', 'name')
    return JsonResponse({'results': list(categories)})


@require_GET
def api_products(request):
    products = Product.objects.select_related('category').all()

    query = request.GET.get('q', '').strip()[:100]
    if query:
        products = products.filter(Q(name__icontains=query) | Q(desc__icontains=query))

    category = request.GET.get('category', '').strip()
    if category:
        try:
            category_id = int(category)
        except ValueError:
            return JsonResponse({'error': 'category must be an integer'}, status=400)
        products = products.filter(category_id=category_id)

    ordering = request.GET.get('ordering', 'name')
    ordering_fields = {
        'name': 'name',
        'price_asc': 'price',
        'price_desc': '-price',
    }
    if ordering not in ordering_fields:
        return JsonResponse({'error': 'ordering must be name, price_asc, or price_desc'}, status=400)

    products = products.order_by(ordering_fields[ordering], 'pk')
    return JsonResponse({
        'count': products.count(),
        'results': [serialize_product(request, product) for product in products],
    })


@require_GET
def api_product_detail(request, product_id):
    try:
        product = Product.objects.select_related('category').get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse(serialize_product(request, product))
