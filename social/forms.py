from django import forms
from .models import Post, Comment, UserProfile
import datetime

class PostForm(forms.ModelForm):
	body = forms.CharField(
		label='',
	 	widget=forms.Textarea(attrs={
	 		'rows' : '3',
	 		'placeholder' : 'Say Something......',
	 		}
	 		)
	 	)
	
	image = forms.ImageField(required=False)
	video = forms.FileField(required=False)

	class Meta:
		model = Post
		fields = ['body', 'image', 'video']

class CommentForm(forms.ModelForm):
	comment = forms.CharField(
		label='',
	 	widget=forms.Textarea(attrs={
	 		'rows' : '1',
	 		'placeholder' : 'Pass a comment...',
	 		}
	 		)
	 	)

	class Meta:
		model = Comment
		fields = ['comment']

class ProfileEditForm(forms.ModelForm):
	birth_date = forms.DateField(
		widget=forms.SelectDateWidget(
			years=range(1900, datetime.date.today().year + 1),
			empty_label=( 'Year', 'Month','Day')
		),
		required=False
	)
	class Meta:
		model = UserProfile
		fields =  ['name', 'bio', 'birth_date', 'school', 'picture',]