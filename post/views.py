from math import ceil
from django.core.cache import cache
from django.shortcuts import render, redirect

from common import rds
from post.models import Post, Tag
from post.models import Comment
from post.helper import page_cache, get_top_n
from post.helper import read_count
from user.helper import login_required
from user.helper import check_perm
# Create your views here.
from user.models import User


@page_cache(53)
def post_list(request):
    page = int(request.GET.get('page', 1))  # 当前页码
    print(page)
    total = Post.objects.count()  # 帖子总数123
    per_page = 10  # 每页帖子数123
    pages = ceil(total / per_page)  # 总页数123

    start = (page - 1) * per_page

    end = start + per_page

    # = SELECT * FROM post where offset start limit 10
    posts = Post.objects.all().order_by('-id')[start:end]  # 惰性加载 懒加载1

    user = User.objects.get(id=888)
    return render(request, 'post_list.html',
                  {'posts': posts, 'pages': range(pages)}, {'user': user})


@login_required
@check_perm('user')
def create_post(request):
    if request.method == 'POST':
        uid = request.session.get('uid')
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(uid=uid, title=title, content=content)
        return redirect('/post/read/?post_id=%s' % post.id)
    return render(request, 'create_post.html', {})


@login_required
def edit_post(request):
    if request.method == "POST":
        post_id = int(request.POST.get('post_id'))
        post = Post.objects.get(id=post_id)
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()

        str_tags = request.POST.get('tags')
        tag_names = [s.strip()
                     for s in str_tags.title().replace(',', ',').split(',')
                     if s.strip()]

        post.update_tags(tag_names)

        # key = 'Post-%s' % post_id
        # cache.set(key, post)  # 修改后的数据存入缓存 更新缓存
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        post_id = request.GET.get('post_id')
        post = Post.objects.get(id=post_id)
        str_tags = ','.join(t.name for t in post.tags())
        return render(request, 'edit_post.html', {'post': post,'tags': str_tags})


@read_count
@page_cache(5)
def read_post(request):
    post_id = int(request.GET.get('post_id'))
    post = Post.objects.get(id=post_id)
    return render(request, 'read_post.html', {'post': post})


@login_required
@check_perm('manager')
def del_post(request):
    post_id = int(request.GET.get('post_id'))
    Post.objects.get(id=post_id).delete()  # 删除数据库的内容
    rds.zrem(b'ReadRank', post_id)  # 同时删除redis上的排行缓存数据

    return redirect('/')


# @page_cache(5)
# def read_post(request):
#     post_id = request.GET.get('post_id')
#     key = 'Post-%s' % post_id
#     # 先从缓存获取
#     post = cache.get(key)
#     # print('Get from cache:', post)
#     if post is None:  # 检查换粗数据是否存在 不存在会返回None  以此判断是否已经存入缓存
#         # 如果不存在则从数据库获取数据  病并讲数据存入缓存
#         post = Post.objects.get(id=post_id)
#         # print('Get from DB:', post)
#         # print('Set to cache')
#         # print('post type:', type(post.content))
#         cache.set('Post-%s' % post.id, post)  # 使用缓存的原因,快
#     return render(request, 'read_post.html', {'post': post})


def search_post(request):
    keyword = request.POST.get('keyword')
    postcc = Post.objects.filter(content__contains=keyword)
    return render(request, 'search_post.html', {'postcc': postcc})


# test post

def top10(request):
    rank_data = get_top_n(10)
    return render(request, 'top10.html', {'rank_data': rank_data})


@login_required
def comment(request):
    uid = request.session['uid']
    post_id = request.POST.get('post_id')
    content = request.POST.get('content')
    Comment.objects.create(uid=uid, post_id = post_id, content=content)
    return redirect('/post/read/?post_id=%s' % post_id)


def tag_filter(request):
    tag_id = int(request.GET.get('tag_id'))
    tag = Tag.objects.get(id=tag_id)
    return render(request, 'tag_filter.html', {'posts': tag.posts()})