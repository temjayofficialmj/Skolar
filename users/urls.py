from django.urls import path
from .views import Homepage, SignUp, PasswordChange

urlpatterns = [
	path('', Homepage.as_view(), name = 'home'),
	path('signup/', SignUp.as_view(), name = 'signup'),
	path('password_change/', PasswordChange.as_view(), name='password_change' )
	]