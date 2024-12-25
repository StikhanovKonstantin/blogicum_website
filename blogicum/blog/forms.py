from django import forms

from .models import Comment


class CommentsForm(forms.ModelForm):
    """Форма для оставления комментариев под постами."""

    class Meta:
        model = Comment
        fields = ('text',)
