from django import forms

from .models import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            "title",
            "content",
            "marca",
            "sub_title",
            "img",
            "price",
            "amount",
        )
