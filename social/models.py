from django.db import models
from django.utils import timezone
#from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Post(models.Model):
	body = models.TextField()
	image = models.ImageField(upload_to='uploads/images', blank=True, null=True)
	video = models.FileField(upload_to='uploads/videos', blank=True, null=True)
	created_on = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likes')
	dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='dislikes')

	def __str__(self):
		return self.body[:10] +  str(self.author)

class Comment(models.Model):
	comment = models.TextField()
	created_on = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	post = models.ForeignKey('Post', on_delete = models.CASCADE)

	def __str__(self):
		return self.comment[:10]

class UserProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
	name = models.CharField(max_length=50, blank=True, null=True)
	bio = models.TextField(max_length=500, null=True, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	school = models.CharField(max_length=100, blank=True, null=True)
	picture = models.ImageField(upload_to='uploads/profiles', default='uploads/profiles/default.jpg')
	followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='followers')
	score = models.IntegerField(default=0)

class WeeklyScore(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	score = models.IntegerField(default=0)
	week_start = models.DateField(default=timezone.now)

	class Meta:
		unique_together = ('user', 'week_start')
	

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


