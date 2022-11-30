from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path
from accounts import views

urlpatterns = [
	path('login/', views.login, name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('signup/', views.signup, name='signup'),
	path('profile/', views.profile, name='profile'),
	path('profile/edit/', views.profile_edit, name='profile_edit'),
	path('password/change/', views.password_change, name='password_change'),
	path('password/find/', views.password_find, name='password_find'),
	path('password/find/email/authenticate/', views.password_find_email_authenticate, 
		name='password_find_email_authenticate'),
	path('password/authenticate/confirm/', views.auth_confirm, name='auth_confirm'),
	path('password/reset/<str:uuid>/', views.password_reset, name='password_reset'),
]