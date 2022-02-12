from django import forms
from tinymce.widgets import TinyMCE
from .models import Post, Comment, Subscribe


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Post
        fields = ('title', 'image', 'content', 'category', 'featured')


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ('email',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'name', 'email')

