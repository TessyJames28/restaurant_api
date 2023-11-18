from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group
from django.http import Http404
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import UserSerializer, OrderItemSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import MenuItemSerializer, CategorySerializer, CartSerializer 
from .models import MenuItem, Order, OrderItem, Category, Cart
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAdminUser
from django.db import transaction
import datetime
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

# Create your views here.
@api_view(['POST'])
def user_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, 201)
    return Response(serializer.errors, 400)


@api_view()
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


class IsManagerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            #allow GET request for all users
            return True
        elif request.user.groups.filter(name="Manager").exists():
            #Allow PUT, PATCH, POST, DELETE request for users in Manager group
            return True
        else:
            raise PermissionDenied("403 - Unauthorized")

class MenuitemView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsManagerPermission]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_field = ['title', 'price', 'featured'] 
    
    
class SingleMenuitemView(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsManagerPermission]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer 
        
    

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

 
@api_view(['POST', 'GET', 'DELETE']) 
@permission_classes([IsAdminUser])  
def managers_group(request, userId=None):
    manager = Group.objects.get(name='Manager')
    if request.method == 'GET':
        users = manager.user_set.all()
        serializers = UserSerializer(users, many=True)
        return Response(serializers.data)
    
    username = request.data['username']
    if username:
        if request.method == 'POST':
            user = get_object_or_404(User, username=username)
            manager.user_set.add(user)
        elif request.method == 'DELETE':
            user = get_object_or_404(User, username=username, id=userId)
            manager.user_set.remove(user)
        return Response({"message":"ok"})
    return Response({"message": "Error"}, status.HTTP_404_NOT_FOUND)
      

@api_view(['POST', 'GET', 'DELETE']) 
@permission_classes([IsAdminUser]) 
def delivery_crew(request, userId=None):
    delivery_crew = Group.objects.get(name='Delivery crew')
    if request.method == 'GET':         
        users = delivery_crew.user_set.all()
        serializers = UserSerializer(users, many=True)
        return Response(serializers.data)
    
    username = request.data['username']
    if username:
        if request.method == 'POST':
            user = get_object_or_404(User, username=username)
            delivery_crew.user_set.add(user)
        elif request.method == 'DELETE':
            user = get_object_or_404(User, username=username, id=userId) 
            delivery_crew.user_set.remove(user)
        return Response({"message":"ok"})
    return Response({"message": "Error"}, status.HTTP_404_NOT_FOUND) 


class CartManagement(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
    
class DestroyCartManagement(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"Message": "Item successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    
    
class OrderView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    ordering_field = ['status', 'date']
    
    def post(self, request, *args, **kwargs):
        user = request.user
        
        # retreive relevant cart item for the users
        cart_items = Cart.objects.filter(user=user)
        
        # calculate total for the order
        total = sum(cart_item.price for cart_item in cart_items)
        
        with transaction.atomic(): # helps to ensure integrity of data
            
            # create a new order instance
            order = Order.objects.create(
                user=user,
                total=total,
                status=False,
                date=datetime.date.today()
            )
            
            # create order items based on cart items
            order_items = []
            for cart_item in cart_items:
                order_item = OrderItem(
                    order = order,
                    menuitem=cart_item.menuitem,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.unit_price,
                    price=cart_item.price
                )
                order_items.append(order_item)
                
            # bulk create order items
            OrderItem.objects.bulk_create(order_items)
            
            # delete cart items
            cart_items.delete()
            
        return Response("Order create and cart items deleted")
    
    def get(self, request, *args, **kwargs):
        user = request.user
        
        # retrieve all order items for the manager
        if user.groups.filter(name='Manager').exists():
            orders = Order.objects.all()
            
        # retrieve all order items for the delivery crew
        elif user.groups.filter(name='Delivery crew').exists():
            orders = Order.objects.filter(delivery_crew=user)
            
        #retrieve all orders
        else:
            orders = Order.objects.filter(user=user)
        
        serializer_data = []
        
        # get order items
        for order in orders:
            order_data = self.get_serializer(order).data
            order_items = OrderItem.objects.filter(order=order)
            order_item_data = OrderItemSerializer(order_items, many=True).data
            order_data['order_items'] = order_item_data
            serializer_data.append(order_data)
            
        
        return Response(serializer_data)
    

class singleOrderItem(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'
    
    def get(self, request, *args, **kwargs):
        user = request.user
        orderId = kwargs['id']
        order = get_object_or_404(Order, id=orderId)
        if order.user != user:
            raise PermissionDenied("Incorrect user for order ID")
        
        orders = Order.objects.filter(id=orderId)
        serializer_data = []
        
        # get order items
        for order in orders:
            order_data = self.get_serializer(order).data
            order_items = OrderItem.objects.filter(order=order)
            order_item_data = OrderItemSerializer(order_items, many=True).data
            order_data['order_items'] = order_item_data
            serializer_data.append(order_data)
            
        
        return Response(serializer_data)
    
    
    def put(self, request, *args, **kwargs):
        user = request.user
        
        if user.groups.filter(name='Manager').exists():
            return super().put(request, *args, **kwargs)
        raise PermissionDenied("You are not authourized to perform this action")
    
    
    def patch(self, request, *args, **kwargs):
        user = request.user
        
        manager = user.groups.filter(name='Manager').exists()
        delivery_crew = user.groups.filter(name='Delivery crew').exists()
        
        if manager or delivery_crew:
            return super().partial_update(request, *args, **kwargs)
        raise PermissionDenied("You are not authourized to perform this action")
    
    
    def destroy(self, request, *args, **kwargs):
        user = request.user
        
        if user.groups.filter(name='Manager').exists():
            return super().destroy(request, *args, **kwargs)
        raise PermissionDenied("You are not authourized to perform this action")
    