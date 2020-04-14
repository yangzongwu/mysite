from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('',views.blog_list,name='blog_list'),
    path('blog-detail/<int:id>',views.blog_detail,name='blog_detail'),
    path('blog-create/',views.blog_create,name='blog_create'),
    path('blog-update/<int:id>',views.blog_update,name='blog_update'),
    path('blog-delete/<int:id>/', views.blog_delete, name='blog_delete'),
    path('classify/<int:id>/', views.classify, name='classify'),
    path('tags/<int:id>/', views.tag, name='tag'),
]