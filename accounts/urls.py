from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path
from accounts import views

urlpatterns = [
	path('login/', views.login, name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('signup/', views.signup, name='signup'),
]