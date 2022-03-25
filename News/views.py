import datetime
import time

import schedule as schedule
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic.edit import BaseDeleteView

from threading import Thread

from .forms import CommentCreationForm, PostCreationForm

from News.forms import UserCreation
from News.models import Post, Comment, Upvote


class Login(LoginView):
    template_name = "login.html"

    def get_success_url(self):
        return "/"


class Register(CreateView):
    form_class = UserCreation
    template_name = "register.html"
    success_url = "/"


class Logout(LogoutView):
    next_page = "/"
    login_url = "login/"


class PostView(ListView):
    model = Post
    paginate_by = 8
    template_name = "index.html"

    def paginate_queryset(self, queryset, page_size):
        r = super(PostView, self).paginate_queryset(queryset, page_size)
        upvote_count = dict()
        for objPost in r[2]:
            upvote_count.update({objPost: Upvote.objects.filter(post=objPost).count()})
        self.extra_context = {"Count": upvote_count}
        return r


class CreatePostView(LoginRequiredMixin, CreateView):
    form_class = PostCreationForm
    template_name = "postcreate.html"
    success_url = "/"

    def form_valid(self, form):
        post_object = form.save(commit=False)
        post_object.author = self.request.user
        post_object.save()
        return super(CreatePostView, self).form_valid(form)


class CommentCreatedView(LoginRequiredMixin, CreateView):
    form_class = CommentCreationForm
    template_name = "comment.html"
    success_url = "/"

    def get(self, request, *args, **kwargs):
        self.extra_context = {
            "comments": Comment.objects.filter(
                Post_id=self.kwargs.get(self.pk_url_kwarg)
            )
        }
        return super(CommentCreatedView, self).get(request)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.Post = Post.objects.get(id=self.kwargs.get(self.pk_url_kwarg))
        comment.save()
        return super().form_valid(form=form)


class UpvotesUpdateView(LoginRequiredMixin, BaseDeleteView):
    model = Post
    success_url = "/"

    def post(self, request, *args, **kwargs):

        post_obj = self.get_object()

        try:
            Upvote.objects.get(author=self.request.user, post=post_obj, flag=True)
        except Upvote.DoesNotExist:
            Upvote.objects.create(author=self.request.user, post=post_obj, flag=True)
        else:
            Upvote.objects.get(
                author=self.request.user, post=post_obj, flag=True
            ).delete()

        return HttpResponseRedirect(self.success_url)


def clear_upvotes():
    Upvote.objects.all().delete()
    print(datetime.datetime.now(), "Upvotes deleted")


def scheduler():
    schedule.every(60 * 60 * 24).seconds.do(clear_upvotes)

    while True:
        schedule.run_pending()
        time.sleep(1)


t = Thread(target=scheduler)
t.start()

