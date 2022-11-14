from django.urls import path
from order import views

app_name = 'order'
urlpatterns = [
	path('pay/', views.order_pay, name='order_pay'),
]