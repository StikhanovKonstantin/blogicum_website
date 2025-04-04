from django import forms

from .models import Comment, Post
from .constants import TEXT_WIDGET_SIZE


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
            'pub_date': forms.DateTimeInput(
                format='%d.%m.%Y %H:%M',
                attrs={
                    'type': 'datetime-local',
                }
            ),
            'text': forms.TextInput(attrs={
                'size': TEXT_WIDGET_SIZE, 'title': 'Ваш текст'}
            )
        }
