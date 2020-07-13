from django.contrib import admin
from .models import Blog, BlogClassify,Tag,view_ip,view_ip_history,BlogDifficulty,BlogClassifyDataStructure,BlogAlgorithm

# Register your models here.

admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(BlogClassify)
admin.site.register(view_ip)
admin.site.register(view_ip_history)
admin.site.register(BlogDifficulty)
admin.site.register(BlogClassifyDataStructure)
admin.site.register(BlogAlgorithm)