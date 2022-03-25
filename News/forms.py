from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from News.models import User, Post, Comment


class UserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)


class PostCreationForm(ModelForm):
    class Meta:
        model = Post
        fields = ("title", "link")


class CommentCreationForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
