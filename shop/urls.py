from django.urls import path
from shop import views

app_name = 'shop'
urlpatterns = [
    path('<int:item_pk>/review/', views.ReviewAPIView.as_view(), name='review'),
    
    path('<str:category_slug>/ALL/', views.CategoryListAllView.as_view(), 
        name='category_list_all'),
    path('<str:category_slug>/<str:sub_category_slug>/', 
        views.CategoryListView.as_view(), name='category_list'),
    path('<str:category_slug>/<str:sub_category_slug>/<str:item_slug>/', 
        views.item_detail, name='item_detail'),
]