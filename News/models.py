from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Author')
    created_at = models.DateTimeField(auto_now=True)
    link = models.URLField(default=not None)


class Comment(models.Model):
    text = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='AuthorComment')
    created_at = models.DateTimeField(auto_now=True)
    Post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='Post')


class Upvote(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='AuthorUpvote')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='PostModel')
    flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
