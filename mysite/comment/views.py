from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from notifications.signals import notify

from blog.models import Blog
from .forms import CommentForm


# 文章评论
@login_required(login_url='/user/login/')
def post_comment(request, id):
    blog = get_object_or_404(Blog, id=id)
    print(id)
    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.blog = blog
            new_comment.user = request.user
            notify.send(
                request.user,
                recipient=blog.author,
                verb='reply',
                target=blog,
                action_object=new_comment
            )
            new_comment.save()
            # 当其参数是一个Model对象时，会自动调用这个Model对象的get_absolute_url()方法
            return redirect(blog)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受POST请求。")
