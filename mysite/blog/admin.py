from django.contrib import admin
from .models import Blog, BlogClassify,Tag

# Register your models here.

admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(BlogClassify)
