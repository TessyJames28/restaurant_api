from django.urls import path   
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('api/users', views.user_view),
    path('token/login/', obtain_auth_token),
    path('api/users/me/', views.profile),
    path('api/menu-items', views.MenuitemView.as_view()),
    path('api/menu-items/<int:pk>', views.SingleMenuitemView.as_view()),
    path('api/category', views.CategoryView.as_view()),
    path('api/groups/manager/users', views.managers_group),
    path('api/groups/manager/users/<userId>', views.managers_group),
    path('api/groups/delivery-crew/users', views.delivery_crew),
    path('api/groups/delivery-crew/users/<userId>', views.delivery_crew),
    path('api/cart/menu-items', views.CartManagement.as_view()),
    path('api/cart/menu-items/<int:pk>', views.DestroyCartManagement.as_view()),
    path('api/orders', views.OrderView.as_view()),
    path('api/orders/<id>', views.singleOrderItem.as_view()),
    
    
]