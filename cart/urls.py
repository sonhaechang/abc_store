from django.urls import path
from cart import views

app_name = 'cart'
urlpatterns = [
    path('', views.cart_list, name='cart_list'),
    path('add/', views.add_cart, name='add_cart'),
    path('delete/<int:item_pk>', views.delete_cart, name='delete_cart'),
]