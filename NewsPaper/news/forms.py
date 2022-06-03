from django.forms import ModelForm
from .models import Post



class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['post_type', 'post_title', 'post_text', 'post_author']
