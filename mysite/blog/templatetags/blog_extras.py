from django import template
from django.db.models import Count

from blog.models import BlogClassify, Blog, Tag

register=template.Library()


@register.inclusion_tag('blog/inclusions/_classify.html',takes_context=True)
def show_classify(context):
    classify_list = BlogClassify.objects.annotate(num_posts=Count('blog')).filter(num_posts__gt=0)
    return {
        'classify_list': classify_list,
        # 'classify_list': BlogClassify.objects.all()
    }


@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_posts=Count('blog')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }