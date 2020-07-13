from django import forms
from blog.models import Blog,BlogClassify,BlogDifficulty,BlogAlgorithm,BlogClassifyDataStructure


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'body', 'avatar',)

class ClassifyAddForm(forms.ModelForm):
    class Meta:
        model=BlogClassify
        fields=('title',)

class BlogDifficultyAddForm(forms.ModelForm):
    class Meta:
        model=BlogDifficulty
        fields=('title',)

class BlogAlgorithmAddForm(forms.ModelForm):
    class Meta:
        model=BlogAlgorithm
        fields=('title',)

class BlogClassifyDataStructureAddForm(forms.ModelForm):
    class Meta:
        model=BlogClassifyDataStructure
        fields=('title',)