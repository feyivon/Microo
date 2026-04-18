from django.db import models
from accounts.models import Account

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length= 30, unique= True)
    slug = models.SlugField(max_length= 30, unique=True)
    description = models.TextField(max_length= 225, blank=True)
    cat_image = models.ImageField(upload_to= 'photos/categories')


    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length= 30, unique=True)
    slug = models.CharField(max_length= 30, unique=True)
    description = models.TextField(max_length= 225, blank=True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2, default= 0.00)
    category = models.ForeignKey(Category, models.CASCADE, related_name = 'product', null = True, blank = True)
    stock = models.IntegerField(default=0)
    product_image = models.ImageField(upload_to= 'photos/products') 
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
class Cart(models.Model):
    cart_id = models.CharField(max_length= 250, blank = True)
    date_added = models.DateField(auto_now_add= True)
    
    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'
        ordering = ['date_added']

    def __str__(self):
        return self.cart_id
    

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE)
    quantity = models.IntegerField(default= 1)
    is_active = models.BooleanField(default=True)


    class Meta:
        verbose_name = 'cartitem'
        verbose_name_plural = 'cartitems'

    def sub_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return self.product.product_name
    

class Order(models.Model):

    STATUS = [
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_METHOD = [
        ('paystack', 'Paystack'),
        ('pay_on_delivery', 'Pay on Delivery'),
    ]

    user           = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    full_name      = models.CharField(max_length=100)
    email          = models.EmailField(max_length=100)
    phone_number   = models.CharField(max_length=20)
    address        = models.CharField(max_length=200)
    city           = models.CharField(max_length=100)
    state          = models.CharField(max_length=100)
    country        = models.CharField(max_length=100)
    total          = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='paystack')
    status         = models.CharField(max_length=20, choices=STATUS, default='New')
    is_ordered     = models.BooleanField(default=False)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.id} — {self.full_name}'
    

class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price    = models.DecimalField(max_digits=10, decimal_places=2)

    def sub_total(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.product.product_name} x {self.quantity}'
