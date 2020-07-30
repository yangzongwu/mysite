import datetime
import markdown
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from lxml import etree

from comment.forms import CommentForm
from comment.models import Comment
from .models import Blog, BlogClassify, Tag, Website_views, view_ip, view_ip_history,\
    BlogDifficulty,BlogClassifyDataStructure,BlogAlgorithm
from .forms import BlogPostForm,ClassifyAddForm,BlogDifficultyAddForm,BlogClassifyDataStructureAddForm,BlogAlgorithmAddForm
from django.contrib.auth.models import User
import requests
from bs4 import BeautifulSoup

def sitemap(request):
    return render(request,'sitemap.xml')

def robots(request):
    return render(request,'robots.txt')

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

def difficulty_add(request):
    if request.method == 'POST':
        new_difficulty_add_form = BlogDifficultyAddForm(request.POST, request.FILES)
        if new_difficulty_add_form.is_valid():
            # commit=False保持数据，暂时不提交
            new_difficulty = new_difficulty_add_form.save(commit=False)
            new_add_difficulty=request.POST['new_difficulty']
            all_difficulty=BlogDifficulty.objects.all()
            difficulty_list=[i.title for i in all_difficulty]
            if new_add_difficulty not in difficulty_list:
                add_difficulty = BlogDifficulty(title=new_add_difficulty)
                add_difficulty.save()
                #new_difficulty.save()
                return redirect("blog:difficulty_add")
            else:
                return HttpResponse("already exist")

        else:
            return  HttpResponse("difficulty is not valid,please refill")
    else:
        difficulty_add_form = BlogDifficultyAddForm()
        difficulties = BlogDifficulty.objects.all()
        context = {'difficulty_add_form': difficulty_add_form, 'difficulties': difficulties,}
        return render(request, 'blog/difficulty_add.html', context)

def datastructrue_add(request):
    if request.method == 'POST':
        datastructure_add_form = BlogClassifyDataStructureAddForm(request.POST, request.FILES)
        if datastructure_add_form.is_valid():
            # commit=False保持数据，暂时不提交
            new_datastructure = datastructure_add_form.save(commit=False)
            new_add_datastructure=request.POST['new_datastructure']
            all_datastructure=BlogClassifyDataStructure.objects.all()
            datastructrue_list=[i.title for i in all_datastructure]
            if new_add_datastructure not in datastructrue_list:
                add_datastructure = BlogClassifyDataStructure(title=new_add_datastructure)
                add_datastructure.save()
                #new_datastructure.save()
                return redirect("blog:datastructrue_add")
            else:
                return HttpResponse("already exist")
        else:
            return  HttpResponse("datastructure is not valid,please refill")
    else:
        datastructrue_add_form = ClassifyAddForm()
        datastructures = BlogClassifyDataStructure.objects.all()
        context = {'classify_add_form': datastructrue_add_form, 'datastructures': datastructures,}
        return render(request, 'blog/datastructure_add.html', context)

def algorithm_add(request):
    if request.method == 'POST':
        algorithm_add_form = BlogAlgorithmAddForm(request.POST, request.FILES)
        if algorithm_add_form.is_valid():
            # commit=False保持数据，暂时不提交
            new_algorithm = algorithm_add_form.save(commit=False)
            new_add_algorithm=request.POST['new_algorithm']
            all_algorithm=BlogAlgorithm.objects.all()
            algorithm_list=[i.title for i in all_algorithm]
            if new_add_algorithm not in algorithm_list:
                add_algorithm = BlogAlgorithm(title=new_add_algorithm)
                add_algorithm.save()
                #new_algorithm.save()
                return redirect("blog:algorithm_add")
            else:
                return HttpResponse("already exist")
        else:
            return  HttpResponse("algorithm is not valid,please refill")
    else:
        algorithm_add_form = BlogAlgorithmAddForm()
        algorithms = BlogAlgorithm.objects.all()
        context = {'algorithm_add_form': algorithm_add_form, 'algorithms': algorithms,}
        return render(request, 'blog/algorithm_add.html', context)

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
            view_ip_history.objects.create(user_ip=user_ip)
            total_views_add()  # 网站总访问量+1
    else:
        # print(user_ip)
        view_ip.objects.create(user_ip=user_ip)
        view_ip_history.objects.create(user_ip=user_ip)
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
            if request.POST['classify'] and request.POST['classify']!= 'none':
                blog.classify = BlogClassify.objects.get(id=request.POST['classify'])
            else:
                blog.classify = None

            if blog.classify.title == 'Leetcode':
                if request.POST['difficulty'] and request.POST['difficulty']!= 'none':
                    blog.difficulty = BlogDifficulty.objects.get(id=request.POST['difficulty'])
                else:
                    blog.difficulty = None
                if request.POST['structure'] and request.POST['structure']!= 'none':
                    blog.datastructrue = BlogClassifyDataStructure.objects.get(id=request.POST['structure'])
                else:
                    blog.datastructrue = None
                if request.POST['algorithm'] and request.POST['algorithm']!= 'none':
                    blog.algorithm = BlogAlgorithm.objects.get(id=request.POST['algorithm'])
                else:
                    blog.algorithm = None
            else:
                blog.tags.clear()
                if request.POST['tag'] and request.POST['tag'] != '':
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
        if blog.classify.title!='Leetcode':
            blog_post_form = BlogPostForm()
            classifies = BlogClassify.objects.all()
            cur_all_tags = blog.tags.all()
            tags = ''
            for curtag in cur_all_tags:
                tags += str(curtag.name) + ','
            tags = tags[:-1]
            context = {'blog': blog, 'blog_post_form': blog_post_form, 'classifies': classifies, 'tags': tags}
            return render(request, 'blog/update.html', context)
        else:
            blog_post_form = BlogPostForm()
            difficulty = BlogDifficulty.objects.all()
            structure = BlogClassifyDataStructure.objects.all()
            classifies = BlogClassify.objects.all()
            algorithm = BlogAlgorithm.objects.all()
            context = {'blog': blog, 'blog_post_form': blog_post_form, 'classifies': classifies,'difficulty': difficulty, 'structure': structure,'algorithm':algorithm}
            return render(request, 'blog/updateleetcode.html', context)

def tag(request, id):
    # 记得在开始部分导入 Tag 类
    t = get_object_or_404(Tag, id=id)
    blogs = Blog.objects.filter(tags=id).order_by('-created_time')
    return render(request, 'blog/list.html', context={'blogs': blogs, "order": "", "search": "","tag":id,"classify":""})


def classify(request, id):
    # 记得在开始部分导入 Tag 类
    t = get_object_or_404(BlogClassify, id=id)
    blogs = Blog.objects.filter(classify=t).order_by('-created_time')
    return render(request, 'blog/list.html', context={'blogs': blogs, "order": "", "search": "","classify":id,"tag":""})


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

def blog_create_leetcode(request):
    if request.method == 'POST':
        blog_post_form = BlogPostForm(request.POST, request.FILES)
        if blog_post_form.is_valid():
            # commit=False保持数据，暂时不提交
            new_blog = blog_post_form.save(commit=False)
            new_blog.author = User.objects.get(id=request.user.id)
            if request.POST['difficulty'] != 'none':
                new_blog.difficulty = BlogDifficulty.objects.get(id=request.POST['difficulty'])
            new_blog.save()
            if request.POST['datastructrue'] != 'none':
                new_blog.datastructrue = BlogClassifyDataStructure.objects.get(id=request.POST['datastructrue'])
            new_blog.save()
            if request.POST['algorithm'] != 'none':
                new_blog.algorithm = BlogAlgorithm.objects.get(id=request.POST['algorithm'])
            new_blog.save()
            new_blog.classify = BlogClassify.objects.get(title='Leetcode')
            new_blog.save()


            return redirect("blog:blog_list_leetcode")
        else:
            return HttpResponse("表单内容有误，请重新填写")
    else:
        blog_post_form = BlogPostForm()
        difficulty = BlogDifficulty.objects.all()
        datastructrue = BlogClassifyDataStructure.objects.all()
        algorithm = BlogAlgorithm.objects.all()
        context = {'blog_post_form': blog_post_form, 'difficulty': difficulty, 'datastructrue': datastructrue,'algorithm':algorithm}
        return render(request, 'blog/create_leetcode.html', context)


def blog_list_leetcode(request):
    get_user_ip(request)
    # 从 url 中提取查询参数
    search = request.POST.get('search')
    order = request.GET.get('order')
    difficulty=request.GET.get('difficulty')
    datastructure=request.GET.get('datastructure')
    algorithm=request.GET.get('algorithm')

    blog_difficulty=BlogDifficulty.objects.all()
    blog_DataStructure=BlogClassifyDataStructure.objects.all()
    blog_Algorithm=BlogAlgorithm.objects.all()
    # 初始化查询集

    classify = BlogClassify.objects.get(title='Leetcode')

    blog_list= Blog.objects.all()
    blog_list = blog_list.filter(classify=classify)

    # 栏目查询集
    if difficulty and difficulty!='None':
        blog_list = blog_list.filter(difficulty=difficulty)

    if datastructure and datastructure!='None':
        blog_list = blog_list.filter(datastructrue=datastructure)

    if algorithm and algorithm!='None':
        blog_list = blog_list.filter(algorithm=algorithm)
    # 搜索查询集
    if search:
        blog_list = blog_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''
    # 查询集排序
    if order == 'total_views':
        blog_list = blog_list.order_by('-total_views')

    paginator = Paginator(blog_list, 20)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {
        'blogs': blogs,
        'order': order,
        'search': search,
        'difficulty':difficulty,
        'datastructure':datastructure,
        'algorithm':algorithm,
        'blog_difficulty':blog_difficulty,
        'blog_DataStructure':blog_DataStructure,
        'blog_Algorithm':blog_Algorithm
    }

    return render(request, 'blog/listleetcode.html', context)


def blog_list(request):
    get_user_ip(request)
    # 从 url 中提取查询参数
    search = request.POST.get('search')
    order = request.GET.get('order')
    classify = request.GET.get('classify')
    tag = request.GET.get('tag')

    # 初始化查询集
    blog_list = Blog.objects.all()

    # 栏目查询集
    if classify is not None and classify.isdigit():
        blog_list = blog_list.filter(classify=classify)

    cur=BlogClassify.objects.get(title='Leetcode')
    blog_list = blog_list.filter(~Q(classify= cur))

    # 标签查询集
    if tag and tag != 'None':
        blog_list = blog_list.filter(tags=tag)

    # 搜索查询集
    if search:
        blog_list = blog_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''
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
    if request.user != blog.author:
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

def ipFinder():
    def ipcheck(ip):
        url = 'https://www.ip.cn/?ip=' + ip
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
        data = ip
        response = requests.get(url=url, params=data, headers=headers)
        page_text = response.text
        tree = etree.HTML(page_text)
        try:
            ip_name = tree.xpath('//div[@id="result"]/div/p[3]/code/text()')[0]
            ip_name = ip_name.split(',')[-1]
            ip_name=ip_name.strip()
        except:
            ip_name = 'local host'
        return ip_name

    user_ip = view_ip.objects.all()
    for user in user_ip[::-1]:
        if not user.national or user.national == 'None':
            user.national=ipcheck(user.user_ip)
            user.save()
        else:
            continue

    user_ip_all = view_ip_history.objects.all()
    for user in user_ip_all[::-1]:
        if not user.national or user.national == 'None':
            user.national = ipcheck(user.user_ip)
            user.save()
        else:
            continue

def user_stat(request):
    ipFinder()
    total_views = Website_views.objects.first()
    user_ip = view_ip.objects.all()
    view_ip_historys=view_ip_history.objects.all().order_by('create_time')

    dict_d={}
    stat_data=[]
    for obj in view_ip_historys:
        ct = obj.create_time
        x=str(ct)
        x=x[:10]
        if x not in dict_d:
            dict_d[x]=1
        else:
            dict_d[x]+=1
        if not stat_data:
            stat_data.append(x)
        else:
            if x!=stat_data[-1]:
                stat_data.append(x)
    listx=stat_data
    listy=[dict_d[x] for x in listx]


    dict_national={}
    for obj in view_ip_historys:
        national=obj.national
        print(national,dict_national)
        if national not in dict_national:
            dict_national[national]=1
        else:
            dict_national[national]+=1
    list_national=[]
    list_count=[]
    for k,v in dict_national.items():
        list_national.append(k)
        list_count.append(v)


    today_dict_national={}
    for obj in user_ip:
        national=obj.national
        if national not in today_dict_national:
            today_dict_national[national]=1
        else:
            today_dict_national[national]+=1
    today_list_national=[]
    today_list_count=[]
    for k,v in today_dict_national.items():
        today_list_national.append(k)
        today_list_count.append(v)


    context = {
        'total_views': total_views,
        'user_ips': user_ip,
        'view_ip_historys':view_ip_historys,
        'listx':listx,
        'listy':listy,
        'list_national':list_national,
        'list_count':list_count,
        'today_list_count':today_list_count,
        'today_list_national':today_list_national,
    }
    return render(request, 'blog/userstat.html', context)

