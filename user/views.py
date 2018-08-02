from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render, redirect
# Create your views here.
from user.models import User
from user.forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()

            # 设置用户登录状态
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            return redirect('/user/info/?uid')
        else:
            return render(request, 'register.html', {'error': form.errors})
    return render(request, 'register.html')


def login(request):
    return render(request, 'login.html', {})


def logout(request):
    request.session.flush()
    return redirect('/user/login/')


def user_info(request):
    uid = request.session.get('uid')
    user = User.objects.get(id=uid)
    return render(request, 'user_info.html', {'user': user})
