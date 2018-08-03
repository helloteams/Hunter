from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
# Create your views here.
from user.models import User
from user.forms import RegisterForm


def register(request):
    # name = settings.SESSION_COOKIE_NAME
    # session_key = request.COOKIES.get(name)

    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()

            # 设置用户登录状态
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            return redirect('/user/info/')
        else:
            return render(request, 'register.html', {'error': form.errors})
    return render(request, 'register.html')


def login(request):
    if request.method == "POST":
        nickname = request.POST.get("nickname")
        password = request.POST.get("password")
        try:
            user = User.objects.get(nickname=nickname)
        except User.DoesNotExist:
            return render(request, "login.html", {"error": '用户不存在，请再次确认后输入'})
        if check_password(password, user.password):
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            return redirect('/user/info/')
        else:
            return render(request, "login.html", {'error': '密码错误'})
    return render(request, 'login.html', {})


def logout(request):
    request.session.flush()
    return redirect('/user/login/')


def user_info(request):
    uid = request.session.get('uid')
    user = User.objects.get(id=uid)
    return render(request, 'user_info.html', {'user': user})
