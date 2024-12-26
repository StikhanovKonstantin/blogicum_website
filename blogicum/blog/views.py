from django.db.models.base import Model as Model
from django.forms import BaseModelForm
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.generic import (
    CreateView, UpdateView, DeleteView, ListView, DetailView
)
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model

from typing import Any

from .models import Post, Category, Comment
from .constants import MAIN_LIMIT
from .forms import CommentsForm, PostForm


User = get_user_model()


class PostListView(ListView):
    """
    Главная страница.
    Показывает 5 последних публикаций.
    """

    model = Post
    template_name = 'blog/index.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            Post.objects.is_category_published()[:MAIN_LIMIT]  # type: ignore
            .select_related('category')
        )


class PostDetailView(DetailView):
    """Показывает страничку отдельного поста."""

    model = Post
    context_object_name = 'post'

    def get_object(self, queryset=None):
        """Переопределяем метод, прописывая собственный запрос."""
        post_id = self.kwargs.get('post_id')
        try:
            return self.model.objects.get(pk=post_id)
        except self.model.DoesNotExist:
            raise Http404('Публикация не найдена')

    def get_context_data(self, **kwargs):
        """
        Добавляем в словарь context новый ключ, значением которого будет
        комментарий для конкретного поста.
        """
        context = super().get_context_data(**kwargs)
        context['form'] = CommentsForm()
        context['comments'] = (
            self.object.comments.select_related('author')  # type: ignore
        )
        return context


class CategoryListView(ListView):
    """Показывает все посты для каждой категории"""

    model = Category
    template_name = 'blog/category.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        """Переопределяем метод, прописывая свой запрос."""
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return (
            Post.objects.published()  # type: ignore
            .filter(category=self.category)
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Добавляем в словарь context доп. ключ - category."""
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class PostCreateView(CreateView):
    """CBV - страничка для создания нового поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.is_published = True
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    """CBV - изменение конкретного поста по ID"""

    model = Post
    fields = '__all__'
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


class PostDeleteView(DeleteView):
    """CBV - удаление конкретного поста по ID"""

    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


class CommentCreateView(CreateView):
    """CBV - создание комментариев под постами."""

    model = Comment
    form_class = CommentsForm
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        """
        Передаём в поле Автор и Номер Поста того, кто отправил запрос
        на создание комментария и Номер Поста из URL.
        """
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class CommentUpdateView(UpdateView):
    model = Comment
    fields = '__all__'
    template_name = 'blog/comment.html'

    def get_object(self, queryset=None):
        post_id = self.kwargs['post_id']
        comment_id = self.kwargs['comment_id']
        return get_object_or_404(self.model, pk=comment_id, post_id=post_id)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class CommentDeleteView(DeleteView):
    """CBV - удаление комментария, используя ID поста и ID комментария."""

    model = Comment
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self, queryset=None):
        """Получаем нужный нужный коммент. по ID поста и ID комментария."""
        post_id = self.kwargs['post_id']
        comment_id = self.kwargs['comment_id']
        return get_object_or_404(self.model, pk=comment_id, post_id=post_id)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class UserDetailView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    paginate_by = 10

    def get_object(self, queryset=None) -> Model:
        username = self.kwargs['username']
        return get_object_or_404(self.model, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        # Получаем посты автора
        context['posts'] = Post.objects.filter(author=profile)
        # Используем их для пагинации
        context['page_obj'] = context['posts']
        return context


class UserUpdateView(UpdateView):
    model = User
    fields = '__all__'
    template_name = 'blog/user.html'

    def get_object(self, queryset=None) -> Model:
        username = self.kwargs['username']
        return get_object_or_404(self.model, username=username)

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.kwargs['username']}
        )
