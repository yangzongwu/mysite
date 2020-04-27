from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Todolist
from .forms import TodolistForm

def todolist_edit(request, id):
    todolist = Todolist.objects.get(id=id)
    if request.method == 'POST':
        todolist_post_form = TodolistForm(data=request.POST)
        if todolist_post_form.is_valid():
            print(request.POST)
            todolist.body = request.POST['body']
            if request.POST['is_done']=='False':
                todolist.is_done = False
            else:
                todolist.is_done=True
            todolist.save()
            return redirect("record:todolist_list")
        else:
            return HttpResponse("表单有问题")
    else:
        todolist_post_form = TodolistForm()
        context = {'todolist': todolist,'todolist_post_form': todolist_post_form}
        return render(request, 'record/update.html', context)


def todolist_delete(request, id):
    todolist = Todolist.objects.get(id=id)
    todolist.delete()
    return redirect('record:todolist_list')


def todolist_add(request):
    if request.method == 'POST':
        todolist_post_form = TodolistForm(data=request.POST)
        if todolist_post_form.is_valid():
            new_todolist = todolist_post_form.save(commit=False)
            new_todolist.save()
            return redirect("record:todolist_list")
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")
    elif request.method == 'GET':
        todolist_form = TodolistForm()
        context = {'form': todolist_form}
        return render(request, 'record/create.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")



# Create your views here.
def todolist_list(request):
    todolist = Todolist.objects.all()
    order = request.GET.get('order')
    if order == 'finished':
        todolist = todolist.filter(is_done=True)
    elif order== 'todolist':
        todolist=todolist.filter(is_done=False)
    else:
        todolist = Todolist.objects.all()

    context = {
        'todolists': todolist,
    }

    return render(request, 'record/todolist.html', context)

