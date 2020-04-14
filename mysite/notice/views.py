from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Blog


class CommentNoticeListView(LoginRequiredMixin,ListView):
    context_object_name = 'notices'
    template_name = 'notice/list.html'
    login_url = '/user/login'

    def get_queryset(self):
        return self.request.user.notifications.unread()

class CommentNoticeUpdateView(View):
    def get(self,request):
        notice_id=request.GET.get('notice_id')
        if notice_id:
            blog=Blog.objects.get(id=request.GET.get('blog_id'))
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(blog)
            # 更新全部通知
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice:list')

