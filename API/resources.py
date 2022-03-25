from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from News.models import User, Upvote, Comment, Post
from API.serializers import (
    UserSerializer,
    PostSerializer,
    PostSerializerList,
    CommentSerializer,
)
from rest_framework.decorators import action


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]

    def list(self, request, *args, **kwargs):
        self.serializer_class = PostSerializerList
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        for i in serializer.data:
            i.update({"Upvotes: ": Upvote.objects.filter(post_id=i.get("id")).count()})

        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def upvote(self, *args, **kwargs):

        post_obj = self.get_object()

        try:
            Upvote.objects.get(author=self.request.user, post=post_obj, flag=True)
        except Upvote.DoesNotExist:
            Upvote.objects.create(author=self.request.user, post=post_obj, flag=True)
        else:
            Upvote.objects.get(
                author=self.request.user, post=post_obj, flag=True
            ).delete()
        return self.list(post_obj)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
