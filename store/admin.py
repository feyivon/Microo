from django.contrib import admin
from store.models import Category, Product, Cart, CartItem, OrderItem, Order

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug')
    prepopulated_fields = {'slug':('category_name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'is_available', 'category', 'modified_at',)
    prepopulated_fields = {'slug':('product_name', )}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')


class OrderAdmin(admin.ModelAdmin):
    list_display  = ('id', 'full_name', 'phone_number', 'total', 'payment_method', 'status', 'created_at')
    list_filter   = ('status', 'payment_method')
    search_fields = ('full_name', 'email', 'phone_number')
    inlines       = [OrderItemInline]


    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)