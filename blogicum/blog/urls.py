from django.urls import path

from . import views

app_name = 'blog'

urlpatterns: list = [
    path('', views.IndexView.as_view(), name='index'),
    path(
        'posts/<int:post_id>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'category/<slug:category_slug>/',
        views.category_posts,
        name='category_posts'
    ),
    path(
        'post/create/',
        views.CreatePostView.as_view(),
        name='create_post'
    ),
    path(
        'post/<int:pk>/edit/',
        views.EditPostView.as_view(),
        name='edit_post'
    ),
    path(
        'post/<int:pk>/delete/',
        views.DeletePostView,
        name='delete_post'
    ),
    path(
        '<int:pk>/comment/',
        views.CommentsCreateView.as_view(),
        name='add_comment'
    ),
    path(
        'profile/<str:username>/',
        views.profile_detail,
        name='profile'
    ),
]
