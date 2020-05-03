from django import forms
from blog.models import Blog,BlogClassify


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'body', 'avatar',)

class ClassifyAddForm(forms.ModelForm):
    class Meta:
        model=BlogClassify
        fields=('title',)