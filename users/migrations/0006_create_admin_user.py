from django.db import migrations
from django.contrib.auth.hashers import make_password
import os

def create_admin_user(apps, schema_editor):
    User = apps.get_model('users', 'CustomUser')

    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
    admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
    admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')

    if not User.objects.filter(email=admin_email).exists():
        User.objects.create(
            email=admin_email,
            username=admin_username,
            password=make_password(admin_password),
            is_staff=True,
            is_superuser=True,
        )
        print(f"✅ Superuser '{admin_username}' created successfully.")
    else:
        print("⚠️ Superuser already exists. Skipping creation.")

def remove_admin_user(apps, schema_editor):
    User = apps.get_model('users', 'CustomUser')
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
    User.objects.filter(email=admin_email).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_customuser_age'),  # match your latest migration name
    ]

    operations = [
        migrations.RunPython(create_admin_user, remove_admin_user),
    ]
