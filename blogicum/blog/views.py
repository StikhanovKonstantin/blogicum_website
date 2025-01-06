from django.db.models.base import Model as Model
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.views.generic import (
    CreateView, UpdateView, DeleteView, ListView, DetailView
)
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import Count
from django.core.paginator import Paginator
from django.utils import timezone

from typing import Any

from .models import Post, Category, Comment
from .forms import CommentsForm, PostForm


User = get_user_model()


class OnlyAuthorMixin(UserPassesTestMixin):
    """
    Миксина - проверят залогинен ли пользователь,
    а также позволяет редактировать/удалять ПОСТЫ только автору.
    """

    def get_login_url(self):
        obj = self.get_object()
        return reverse_lazy('blog:post_detail', kwargs={'post_id': obj.pk})

    def handle_no_permission(self):
        return redirect(self.get_login_url())

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class OnlyUsernameMixin(UserPassesTestMixin):
    """
    Миксина - проверят залогинен ли пользователь,
    а также позволяет редактировать/удалять КОММЕНТАРИИ только автору.
    """

    def test_func(self):
        object = self.get_object()
        return object == self.request.user


class PostListView(ListView):
    """
    Главная страница.
    Показывает 10 публикаций на 1-й странице.
    """

    model = Post
    template_name = 'blog/index.html'
    paginate_by = 10
    queryset = (
        Post.objects.is_category_published(
        ).select_related(
            'category', 'location', 'author'
        ).annotate(
            comment_count=Count('comments')
        ).order_by(
            '-pub_date'
        )
    )


class PostDetailView(DetailView):
    """Показывает страничку отдельного поста."""

    model = Post
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post_id = self.kwargs.get('post_id')

        # Получаем пост без учета даты публикации и доступности категории
        post = get_object_or_404(
            self.model.objects.select_related('category'),
            pk=post_id
        )

        # Проверяем права доступа: неопубликованные посты
        #  доступны только автору.
        if not post.is_published or (
            post.category and not post.category.is_published
        ):
            if post.author != self.request.user:
                raise Http404('Публикация не найдена')

        # Проверяем дату публикации, ошибки не будет если автор
        if post.pub_date > timezone.now() and post.author != self.request.user:
            raise Http404('Публикация не найдена')

        return post

    def get_context_data(self, **kwargs):
        """
        Добавляем в словарь context новый ключ, значением которого будет
        комментарий для конкретного поста.
        """
        context = super().get_context_data(**kwargs)
        context['form'] = CommentsForm()
        context['comments'] = (
            self.object.comments.select_related('author')
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
            Post.objects.published(
            ).filter(
                category=self.category
            ).annotate(
                comment_count=Count('comments')
            ).order_by('-pub_date')
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Добавляем в словарь context доп. ключ - category."""
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """CBV - страничка для создания нового поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        # Связываем пост с текущим пользователем
        # и устанавливаем флаг публикации.
        form.instance.author = self.request.user
        if form.instance.pub_date > timezone.now():
            form.instance.is_published = False
        else:
            form.instance.is_published = True
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(
            'blog:profile', kwargs={
                'username': self.request.user.username
            }
        )


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    """CBV - изменение конкретного поста по ID"""

    model = Post
    fields = 'title', 'text', 'category', 'image'
    template_name = 'blog/create.html'

    def get_success_url(self) -> str:
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.object.pk}
        )


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    """CBV - удаление конкретного поста по ID"""

    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


class CommentCreateView(LoginRequiredMixin, CreateView):
    """CBV - создание комментариев под постами2."""

    model = Comment
    form_class = CommentsForm
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        """
        Передаём в поле Автор и Номер Поста того, кто отправил запрос
        на создание комментария и Номер Поста из URL.
        """
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class CommentUpdateView(OnlyAuthorMixin, UpdateView):
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


class CommentDeleteView(OnlyAuthorMixin, DeleteView):
    """CBV - удаление комментария, используя ID поста и ID комментария."""

    model = Comment
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self, queryset=None):
        """Получаем нужный коммент. по ID поста и ID комментария."""
        post_id = self.kwargs['post_id']
        comment_id = self.kwargs['comment_id']
        return get_object_or_404(self.model, pk=comment_id, post_id=post_id)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class UserDetailView(DetailView):
    """CBV - страница просмотра профиля."""

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
        # Получаем посты автора.
        if self.request.user == profile:
            # Если пользователь - автор, показываем все посты.
            posts = Post.objects.filter(author=profile)
        else:
            # Иначе показываем только опубликованные.
            posts = Post.objects.filter(author=profile, is_published=True)
        context['posts'] = posts.order_by(
            '-pub_date'
        ).annotate(
            comment_count=Count('comments')
        )
        paginator = Paginator(context['posts'], self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        return context


class UserUpdateView(OnlyUsernameMixin, UpdateView):
    """Форма для редактирования профиля."""

    model = User
    fields = 'first_name', 'last_name', 'username', 'email'
    template_name = 'blog/user.html'

    def get_object(self, queryset=None) -> Model:
        username = self.kwargs['username']
        return get_object_or_404(self.model, username=username)

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.kwargs['username']}
        )
