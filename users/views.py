from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from .forms import CustomUserCreation
from .models import CustomUser
from django.views import View

# Create your views here.
class Homepage(View):
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('postlist')  # logged-in users skip homepage
		return render(request, 'home.html')  # guests see landing page

class SignUp(CreateView):
	form_class = CustomUserCreation
	success_url = reverse_lazy('login')
	template_name = 'signup.html'

class PasswordChange(TemplateView):
	template_name = 'registration/password_change_form.html'
