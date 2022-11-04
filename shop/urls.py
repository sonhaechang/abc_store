from django.urls import path, re_path
from shop import views

app_name = 'shop'
urlpatterns = [
    re_path(r'^(?P<category_slug>[-\w]+)/all/$', 
        views.CategoryListAllView.as_view(), name='category_list_all'),
    re_path(r'^(?P<category_slug>[-\w]+)/(?P<sub_category_slug>[-\w]+)/$', 
        views.CategoryListView.as_view(), name='category_list'),
]