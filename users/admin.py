from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreation, CustomUserChange
from .models import CustomUser

# Register your models here.
class CustomAdmin(UserAdmin):
	add_form = CustomUserCreation
	form = CustomUserChange
	model = CustomUser
	list_display = ['email', 'username', 'is_staff',]

admin.site.register(CustomUser, CustomAdmin)
