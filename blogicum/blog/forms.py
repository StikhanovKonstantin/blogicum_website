from django import forms

from .models import Comments


class CommentsForm(forms.ModelForm):
    """Форма для оставления комментариев под постами."""

    class Meta:
        model = Comments
        fields = ('text',)