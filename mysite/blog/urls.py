from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('',views.blog_list,name='blog_list'),
    path('sitemap.xml',views.sitemap,name='sitemap'),
    path('blog_list_leetcode',views.blog_list_leetcode,name='blog_list_leetcode'),
    path('blog_create_leetcode/',views.blog_create_leetcode,name='blog_create_leetcode'),
    path('blog-detail/<int:id>',views.blog_detail,name='blog_detail'),
    path('blog-create/',views.blog_create,name='blog_create'),
    path('blog-update/<int:id>',views.blog_update,name='blog_update'),
    path('blog-delete/<int:id>/', views.blog_delete, name='blog_delete'),
    path('classify/<int:id>/', views.classify, name='classify'),
    path('tags/<int:id>/', views.tag, name='tag'),
    path('user_stat/',views.user_stat,name='user_stat'),
    path('classify_add/',views.classify_add,name='classify_add'),
    path('difficulty_add/',views.difficulty_add,name='difficulty_add'),
    path('datastructrue_add/',views.datastructrue_add,name='datastructrue_add'),
    path('algorithm_add/',views.algorithm_add,name='algorithm_add'),

]
