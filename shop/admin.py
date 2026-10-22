from django.contrib import admin
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.order import Order, OrderItem

# Register your models here.
class Categoryinfo(admin.ModelAdmin):
    list_display=["name"]

class Productinfo(admin.ModelAdmin):
    list_display=["name","category","price"]

class Customerinfo(admin.ModelAdmin):
    list_display=["first_name","last_name","email"]

admin.site.register(Product,Productinfo)
admin.site.register(Category,Categoryinfo)
admin.site.register(Customer,Customerinfo)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "unit_price", "quantity")

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "total", "created_at")
    list_filter = ("created_at",)
    inlines = (OrderItemInline,)

admin.site.register(Order, OrderAdmin)
