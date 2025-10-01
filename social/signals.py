from django.conf import settings
from django.db.models.signals import post_save
from .models import Post, WeeklyScore
from django.dispatch import receiver
from django.utils.timezone import now
from datetime import timedelta

# @receiver(post_save, sender=Post)
# def update_user_score(sender, instance, created, **kwargs):
# 	if created:
# 		user = instance.author
# 		user.score += 10
# 		user.save()

def get_week_start():
	today = now().date()
	return today - timedelta(days=today.weekday())

@receiver(post_save, sender=Post)
def update_weekly_score(sender, instance, created, **kwargs):
	if created:
		week_start = get_week_start()
		user = instance.author
		score_obj, _= WeeklyScore.objects.get_or_create(
			user=user,
			week_start=week_start
			)
		score_obj.score += 10
		score_obj.save()
		# user.score += 10
		# user.save()