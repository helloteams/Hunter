
#
# def get_wb_user_show(access_token,uid):
#     args = settings.WB_USER_SHOW_ARGS.copy()
from django.shortcuts import render
from django.shortcuts import redirect
from user.models import User


def login_required(view_func):
    def wrapper(request):
        uid = request.session.get('uid')
        if uid is None:
            return redirect('/user/login/')
        else:
            return view_func(request)
    return wrapper


def check_perm(perm_name):
    def deco(view_func):
        def wrapper(request):
            uid = request.session['uid']
            user = User.objects.get(id=uid)

            if user.has_perm(perm_name):
                return view_func(request)
            else:
                return render(request, 'blockers.html',)
        return wrapper
    return deco


