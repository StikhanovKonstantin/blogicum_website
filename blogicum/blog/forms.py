from django import forms

from .models import Comment, Post


class CommentsForm(forms.ModelForm):
    """Форма для оставления комментариев под постами."""

    class Meta:
        model = Comment
        fields = ('text',)


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            'title', 'text', 'pub_date', 'location', 'category', 'image'
        )
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'text': forms.TextInput(attrs={'size': 10, 'title': 'Ваш текст'})
        }
