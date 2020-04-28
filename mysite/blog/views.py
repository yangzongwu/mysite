import markdown
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from comment.forms import CommentForm
from comment.models import Comment
from .models import Blog, BlogClassify, Tag
from .forms import BlogPostForm
from django.contrib.auth.models import User


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
                rep=set()
                for obj in Tag.objects.all():
                    rep.add(obj.name)
                for cur in curs:
                    if not cur in rep:
                        rep.add(cur)
                        new_tag = Tag(name = cur)
                        new_tag.save()
                    addtag=Tag.objects.get(name=cur)
                    blog.tags.add(addtag)
                    blog.save()
            blog.save()

            return redirect('blog:blog_detail', id=id)
        else:
            return HttpResponse("表单有问题")
    else:
        blog_post_form = BlogPostForm()
        classifies = BlogClassify.objects.all()
        tags=''
        context = {'blog': blog, 'blog_post_form': blog_post_form, 'classifies': classifies,'tags':tags }
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
                rep=set()
                for obj in Tag.objects.all():
                    rep.add(obj.name)
                for cur in curs:
                    if not cur in rep:
                        rep.add(cur)
                        new_tag = Tag(name = cur)
                        new_tag.save()
                    addtag=Tag.objects.get(name=cur)
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
