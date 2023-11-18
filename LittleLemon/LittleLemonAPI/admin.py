from django.contrib import admin
from .models import Category, MenuItem, Order, OrderItem, Cart
from django.contrib.auth.models import User

# Register your models here.
admin.register(Category)
admin.register(MenuItem)
admin.register(Cart)
admin.register(Order)
admin.register(OrderItem)
