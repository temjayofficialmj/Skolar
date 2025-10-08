from django.urls import path
from . import views
from .views import (
	PostList,
	PostDetail,
	PostUpdate,
	PostDelete,
	CommentDelete,
	Profile,
	ProfileEdit,
	AddFollower,
	RemoveFollower,
	AddLike,
	AddDislike,
	Search,
	PostCreate,
	Explore,
	Followers,
	)

urlpatterns = [
	path('', PostList.as_view(), name = 'postlist'),
	# path('post/create/', views.PostCreate, name = 'postcreate'),
	path('post/create/', PostCreate.as_view(), name = 'postcreate'),
	path('post/<int:pk>/', PostDetail.as_view(), name = 'postdetail'),
	path('post/<int:post_pk>/comment/delete/<int:pk>', CommentDelete.as_view(), name = 'commentdelete' ),
	path('post/<int:pk>/like', AddLike.as_view(), name = 'like'),
	path('post/<int:pk>/dislike', AddDislike.as_view(), name = 'dislike'),
	path('profile/<int:pk>', Profile.as_view(), name = 'profileview'),
	path('profile/edit/<int:pk>/', ProfileEdit.as_view(), name = 'profile-edit'),
	path('profile/<int:profile_pk>/post/delete/<int:pk>/', PostDelete.as_view(), name = 'postdelete'),
	path('profile/<int:profile_pk>/post/edit/<int:pk>/', PostUpdate.as_view(), name = 'postupdate'),
	path('profile/<int:pk>/followers/', Followers.as_view(), name = 'followers_list'),
	path('profile/<int:pk>/followers/add', AddFollower.as_view(), name = 'add-follower'),
	path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name = 'remove-follower'),
	path('search/', Search.as_view(), name = 'profile-search'),
	path('explore/', Explore.as_view(), name = 'explore'),
	path('leaderboard/', views.leaderboard_view, name = 'lead')
	] 