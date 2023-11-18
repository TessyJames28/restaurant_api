from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MenuItem, Order, Cart, OrderItem, Category


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='username') # map 'username' to 'name'
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        
    def create(self, validated_data):
        # Extra and remove the 'password' firld from the validated data
        password = validated_data.pop('password')
        
        # create the user with the remaining validated data
        user = User.objects.create_user(**validated_data)
        
        # set user's password separately
        user.set_password(password)
        user.save()
        
        return user
    
    
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title'] 
        

# class CustomSmallIntegerField(serializers.Field):
#     def to_represent(self, value):
#         return int(value) # convert to JSOn serializable data
    
#     def to_internal_value(self, data):
#         return int(data) # convert incoming data to the internal value type

class CartSerializer(serializers.ModelSerializer):
    # quantity = CustomSmallIntegerField()
    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']
        
    def create(self, validated_data):
        validated_data['price'] = validated_data['unit_price'] * validated_data['quantity']
        return super().create(validated_data)
    

class OrderItemSerializer(serializers.ModelSerializer):
    # quantity = CustomSmallIntegerField()
    price = serializers.SerializerMethodField(method_name='total_price')
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price']
        
    def total_price(self, product:OrderItem):
        return product.unit_price * product.quantity
    
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
