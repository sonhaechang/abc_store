from django.urls import path
from order import views

app_name = 'order'
urlpatterns = [
	path('list/', views.OrderListView.as_view(), name='order_list'),
	path('pay/', views.order_pay, name='order_pay'),
	path('save/session/', views.order_item_save_in_session, name='order_item_save_in_session'),
	path('complete/mobile/', views.order_complete_mobile, name='order_complete_mobile'),
	path('complete/<str:merchant_uid>/', views.order_complete, name='order_complete'),
	path('detail/<str:merchant_uid>/', views.order_detail, name='order_detail'),
]