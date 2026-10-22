from django.shortcuts import render
from django.db.models import Q
from shop.models.product import Product
from shop.models.category import Category
from django.views import View

#class based view
class home(View):
    def get(self,request):
        categories = Category.objects.order_by('name')
        selected_category = request.GET.get('category', '').strip()
        search_query = request.GET.get('q', '').strip()[:100]
        ordering = request.GET.get('ordering', 'name')
        ordering_options = {
            'name': 'name',
            'price_asc': 'price',
            'price_desc': '-price',
        }
        if ordering not in ordering_options:
            ordering = 'name'
        products = Product.objects.select_related('category').all()

        if selected_category:
            try:
                category_id = int(selected_category)
            except ValueError:
                category_id = None

            if category_id is not None and Category.objects.filter(pk=category_id).exists():
                products = products.filter(category_id=category_id)
                selected_category = str(category_id)
            else:
                selected_category = ''

        if search_query:
            products = products.filter(Q(name__icontains=search_query) | Q(desc__icontains=search_query))
        products = products.order_by(ordering_options[ordering], 'pk')

        data = {
            'products': products,
            'categories': categories,
            'selected_category': selected_category,
            'search_query': search_query,
            'selected_ordering': ordering,
        }
        return render(request, 'index.html', data)
