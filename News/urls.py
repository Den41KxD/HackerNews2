from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter

from .views import Login, Register, Logout, PostView, CommentCreatedView, UpvotesUpdateView, CreatePostView

from API.resources import UserViewSet, PostViewSet, CommentViewSet

router = SimpleRouter()
router.register('user', UserViewSet)
router.register('post', PostViewSet)
router.register('comment', CommentViewSet)


urlpatterns = [

    path('', PostView.as_view(), name='index'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('comment/<int:pk>/', CommentCreatedView.as_view(), name='comment'),
    path('update/<int:pk>/', UpvotesUpdateView.as_view(), name='update'),
    path('createpost/', CreatePostView.as_view(), name='createPost'),
    path('api/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token)

]
