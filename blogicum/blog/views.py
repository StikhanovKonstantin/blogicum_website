from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from .models import Post, Category
from .constants import MAIN_LIMIT


User = get_user_model()


def index(request):
    """
    Главная страница.
    Показывает 5 последних публикаций.
    """
    post_list = (
        Post.objects.is_category_published()[:MAIN_LIMIT]
        .select_related('category')
    )
    context: dict = {
        'post_list': post_list
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    """Показывает страничку отдельного поста."""
    post = Post.objects.get_post_detail(post_id)
    if post is None:
        raise Http404('Публикация не найдена')
    context = {
        'post': post
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """Показывает посты для каждой категории"""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    post_list = Post.objects.published().filter(category=category)

    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, 'blog/category.html', context)


class CreatePostView(CreateView):
    """CBV - страничка для создания нового поста."""

    model = Post
    fields = '__all__'
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


class EditPostView(UpdateView):
    """CBV - изменение конкретного поста."""

    model = Post
    fields = '__all__'
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


class DeletePostView(DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


class EditProfileView(UpdateView):
    ...


def profile_detail(request, username):
    """Страничка профиля - показывает профиль конкретного пользователя."""
    profile = get_object_or_404(
        User,
        username=username
    )
    context: dict = {
        'profile': profile
    }
    return render(request, 'blog/profile.html', context)
