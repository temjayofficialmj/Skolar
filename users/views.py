from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from .forms import CustomUserCreation
from .models import CustomUser

# Create your views here.
class Homepage(TemplateView):
	template_name = 'home.html'

class SignUp(CreateView):
	form_class = CustomUserCreation
	success_url = reverse_lazy('login')
	template_name = 'signup.html'

class PasswordChange(TemplateView):
	template_name = 'registration/password_change_form.html'
