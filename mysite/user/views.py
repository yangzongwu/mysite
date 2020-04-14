from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm
from .forms import ProfileForm
from .models import Profile


@login_required(login_url='/user/login/')
def profile_edit(request,id):
    user=User.objects.get(id=id)
    # user_id是外键自动生成的字段，用来表征两个数据表的关联。
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method=='POST':
        if request.user!=user:
            return HttpResponse("you do not have permition")
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_cd=profile_form.cleaned_data
            profile.phone=profile_cd['phone']
            profile.bio=profile_cd['bio']
            if 'avatar' in request.FILES:
                print('x')
                profile.avatar = profile_cd["avatar"]
            profile.save()
            return redirect('user:edit',id=id)
        else:
            return HttpResponse("something fill wrong")
    elif request.method=='GET':
        profile_form=ProfileForm()
        context = {'profile_form': profile_form, 'profile': profile, 'user': user}
        return render(request, 'user/edit.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")

# Create your views here.
@login_required(login_url='/user/login/')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        if request.user == user:
            logout(request)
            user.delete()
            return redirect('blog:blog_list')
        else:
            return HttpResponse("you do not have permit")
    else:
        return HttpResponse("only POST method")


def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据后立即登录并返回博客列表页面
            login(request, new_user)
            return redirect("blog:blog_list")
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'user/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


def user_logout(request):
    logout(request)
    return redirect('blog:blog_list')


def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            # authenticate()方法验证用户名称和密码是否匹配
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # login()方法实现用户登录，将用户数据保存在session中
                login(request, user)
                return redirect('blog:blog_list')
            else:
                return HttpResponse("用户名密码不匹配")
        else:
            return HttpResponse("用户吗密码不合法")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'user/login.html', context)
    else:
        return HttpResponse("please use GET or POST method")
