from django.urls import path
from order import views

app_name = 'order'
urlpatterns = [
	path('list/', views.OrderListView.as_view(), name='order_new'),
	path('pay/', views.order_pay, name='order_pay'),
	path('complete/<str:merchant_uid>/', views.order_complete, name='order_complete'),
]