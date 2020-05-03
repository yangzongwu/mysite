import datetime

import markdown
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from comment.forms import CommentForm
from comment.models import Comment
from .models import Blog, BlogClassify, Tag, Website_views, view_ip
from .forms import BlogPostForm,ClassifyAddForm
from django.contrib.auth.models import User


def classify_add(request):
    if request.method == 'POST':
        classify_add_form = ClassifyAddForm(request.POST, request.FILES)
        if classify_add_form.is_valid():
            # commit=False保持数据，暂时不提交
            new_classify = classify_add_form.save(commit=False)
            new_add_classify=request.POST['new_classify']
            all_classify=BlogClassify.objects.all()
            claasify_list=[i.title for i in all_classify]
            if new_add_classify not in claasify_list:
                add_classify = BlogClassify(title=new_add_classify)
                add_classify.save()
                new_classify.save()
                return redirect("blog:blog_list")
            else:
                return HttpResponse("already exist")
        else:
            return  HttpResponse("classify is not valid,please refill")
    else:
        classify_add_form = ClassifyAddForm()
        classifies = BlogClassify.objects.all()
        context = {'classify_add_form': classify_add_form, 'classifies': classifies,}
        return render(request, 'blog/classify_add.html', context)

def get_user_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:  # 获取用户真实IP地址
        user_ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        user_ip = request.META['REMOTE_ADDR']
    obj = view_ip.objects.first()
    if not obj == None:  # 判断数据表是否为空
        ct = obj.create_time
        if not ct.month == datetime.datetime.now().month or not ct.day == datetime.datetime.now().day:  # 判断表中数据是否为当日访问
            objs = view_ip.objects.all()  # 不是当日访问则迭代删除表中数据
            for i in objs:
                i.delete()
        if not view_ip.objects.filter(user_ip=user_ip):  # 判断当日用户是否已经访问过本网站
            view_ip.objects.create(user_ip=user_ip)  # 将用户IP存入数据库
            total_views_add()  # 网站总访问量+1
    else:
        # print(user_ip)
        view_ip.objects.create(user_ip=user_ip)
        total_views_add()


def total_views_add():
    obj = Website_views.objects.first()
    if obj == None:
        Website_views.objects.create(views=1)
    else:
        total_views = Website_views.objects.first()
        total_views.views = total_views.views + 1
        total_views.save()


def blog_delete(request, id):
    blog = Blog.objects.get(id=id)
    if request.user != blog.author:
        return HttpResponse("抱歉，你无权删除这篇文章。")
    blog = Blog.objects.get(id=id)
    blog.delete()
    return redirect('blog:blog_list')


def blog_update(request, id):
    blog = Blog.objects.get(id=id)
    if request.user != blog.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    if request.method == 'POST':
        blog_post_form = BlogPostForm(data=request.POST)
        if blog_post_form.is_valid():
            blog.title = request.POST['title']
            blog.body = request.POST['body']
            if request.POST['classify'] != 'none':
                blog.classify = BlogClassify.objects.get(id=request.POST['classify'])
            else:
                blog.classify = None

            blog.tags.clear()
            if request.POST['tag'] != '':
                curs = request.POST['tag'].split(',')
                rep = set()
                for obj in Tag.objects.all():
                    rep.add(obj.name)
                for cur in curs:
                    if cur != '' and not cur in rep:
                        rep.add(cur)
                        new_tag = Tag(name=cur)
                        new_tag.save()
                    if cur:
                        addtag = Tag.objects.get(name=cur)
                        blog.tags.add(addtag)
                        blog.save()
            blog.save()

            return redirect('blog:blog_detail', id=id)
        else:
            return HttpResponse("表单有问题")
    else:
        blog_post_form = BlogPostForm()
        classifies = BlogClassify.objects.all()
        cur_all_tags = blog.tags.all()
        tags = ''
        for curtag in cur_all_tags:
            tags += str(curtag.name) + ','
        tags = tags[:-1]
        context = {'blog': blog, 'blog_post_form': blog_post_form, 'classifies': classifies, 'tags': tags}
        return render(request, 'blog/update.html', context)


def tag(request, id):
    # 记得在开始部分导入 Tag 类
    t = get_object_or_404(Tag, id=id)
    blogs = Blog.objects.filter(tags=id).order_by('-created_time')
    return render(request, 'blog/list.html', context={'blogs': blogs, "order": "", "search": ""})


def classify(request, id):
    # 记得在开始部分导入 Tag 类
    t = get_object_or_404(BlogClassify, id=id)
    blogs = Blog.objects.filter(classify=t).order_by('-created_time')
    return render(request, 'blog/list.html', context={'blogs': blogs, "order": "", "search": ""})


def blog_create(request):
    if request.method == 'POST':
        blog_post_form = BlogPostForm(request.POST, request.FILES)
        if blog_post_form.is_valid():
            # commit=False保持数据，暂时不提交
            new_blog = blog_post_form.save(commit=False)
            new_blog.author = User.objects.get(id=request.user.id)
            if request.POST['classify'] != 'none':
                new_blog.classify = BlogClassify.objects.get(id=request.POST['classify'])
            new_blog.save()

            if request.POST['tag'] != 'none':
                curs = request.POST['tag'].split(',')
                rep = set()
                for obj in Tag.objects.all():
                    rep.add(obj.name)
                for cur in curs:
                    if cur != '' and not cur in rep:
                        rep.add(cur)
                        new_tag = Tag(name=cur)
                        new_tag.save()
                    if cur:
                        addtag = Tag.objects.get(name=cur)
                        new_blog.tags.add(addtag)
                        new_blog.save()

            return redirect("blog:blog_list")
        else:
            return HttpResponse("表单内容有误，请重新填写")
    else:
        blog_post_form = BlogPostForm()
        classifies = BlogClassify.objects.all()
        tags = Tag.objects.all()
        context = {'blog_post_form': blog_post_form, 'classifies': classifies, 'tags': tags}
        return render(request, 'blog/create.html', context)


def blog_list(request):
    get_user_ip(request)
    # 从 url 中提取查询参数
    search = request.GET.get('search')
    order = request.GET.get('order')
    classify = request.GET.get('classify')
    tag = request.GET.get('tag')

    # 初始化查询集
    blog_list = Blog.objects.all()

    # 搜索查询集
    if search:
        blog_list = blog_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

    # 栏目查询集
    if classify is not None and classify.isdigit():
        blog_list = blog_list.filter(classify=classify)

    # 标签查询集
    if tag and tag != 'None':
        blog_list = blog_list.filter(tags__name__in=[tag])

    # 查询集排序
    if order == 'total_views':
        blog_list = blog_list.order_by('-total_views')

    paginator = Paginator(blog_list, 5)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {
        'blogs': blogs,
        'order': order,
        'search': search,
        'classify': classify,
        'tag': tag,
    }

    return render(request, 'blog/list.html', context)


def blog_detail(request, id):
    get_user_ip(request)
    blog = Blog.objects.get(id=id)
    comments = Comment.objects.filter(blog=id)
    blog.total_views += 1
    blog.save(update_fields=['total_views'])

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc', ])
    blog.body = md.convert(blog.body)
    blog.toc = md.toc
    comment_form = CommentForm()
    context = {
        'blog': blog, 'toc': md.toc, 'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/detail.html', context)


def user_stat(request):
    total_views = Website_views.objects.first()
    user_ip = view_ip.objects.all()
    context = {
        'total_views': total_views,
        'user_ips': user_ip,
    }
    return render(request, 'blog/userstat.html', context)
