from rest_framework import serializers
from rest_framework.authtoken.models import Token

from News.models import User, Comment, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get("password"))
        user.save()
        Token.objects.create(user=user)
        return user


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "link", "created_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        new_app = Post.objects.create(**validated_data, author=request.user)
        new_app.save()
        return new_app


class PostSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "link", "created_at", "author"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["text", "Post_id"]

    def create(self, validated_data):
        request = self.context.get("request")
        new_comment = Comment.objects.create(
            **validated_data,
            author=request.user,
            Post=Post.objects.get(id=request.data.get("Post_id"))
        )
        new_comment.save()
        return new_comment
