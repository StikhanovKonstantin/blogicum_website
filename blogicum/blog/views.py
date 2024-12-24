from django.shortcuts import render, get_object_or_404
from django.http import Http404

from .models import Post, Category
from .constants import MAIN_LIMIT


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
