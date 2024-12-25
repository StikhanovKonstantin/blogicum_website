from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import (
    CreateView, UpdateView, DeleteView, ListView, DetailView
)
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model

from .models import Post, Category, Comments
from .constants import MAIN_LIMIT
from .forms import CommentsForm


User = get_user_model()


class IndexView(ListView):
    """
    Главная страница.
    Показывает 5 последних публикаций.
    """
    
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            Post.objects.is_category_published()[:MAIN_LIMIT]
            .select_related('category')
        )
        


class PostDetailView(DetailView):
    """Показывает страничку отдельного поста."""

    model = Post
    context_object_name = 'post'

    def get_object(self, queryset=None):
        # Переопределяем метод, чтобы обрабатывать случай,
        # когда объект не найден
        post_id = self.kwargs.get('post_id')
        try:
            return self.model.objects.get(pk=post_id)
        except self.model.DoesNotExist:
            raise Http404('Публикация не найдена')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentsForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context

    # post = Post.objects.get_post_detail(post_id)
    # if post is None:
    #     raise Http404('Публикация не найдена')
    # context = {
    #     'post': post
    # }
    # return render(request, 'blog/detail.html', context)


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
    """CBV - изменение конкретного поста по ID"""

    model = Post
    fields = '__all__'
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


class DeletePostView(DeleteView):
    """CBV - удаление конкретного поста по ID"""
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


class CommentsCreateView(CreateView):
    """CBV - оставление комментариев под постами."""
    object = None
    model = Comments
    form_class = CommentsForm

    def dispatch(self, request, *args, **kwargs):
        # В этом методе мы получаем объект 
        self.object = get_object_or_404(
            Post, pk=kwargs['pk']
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.object
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:posts', kwargs={'post_id': self.post.pk})


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
