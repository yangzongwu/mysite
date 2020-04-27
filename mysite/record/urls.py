from django.urls import path
from . import views

app_name = 'record'
urlpatterns = [
    path('todolist_list/', views.todolist_list, name='todolist_list'),
    path('todolist_add/', views.todolist_add, name='todolist_add'),
    path('todolist_edit/<int:id>', views.todolist_edit, name='todolist_edit'),
    path('todolist_delete/<int:id>', views.todolist_delete, name='todolist_delete'),
]