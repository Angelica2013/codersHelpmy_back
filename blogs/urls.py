from django.urls import path, include
from .views import PostListCreateView, CommentCreateView, CommentDetailView, RegisterView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('comments/<int:post_id>/', CommentCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:post_id>/<int:parent_id>/', CommentCreateView.as_view(), name='comment-reply-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]

