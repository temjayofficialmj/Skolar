from users.models import CustomUser

for user in CustomUser.objects.all():
	user.score = user.post_set.count() * 10
	user.save()

