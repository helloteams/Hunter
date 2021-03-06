from django.shortcuts import render,redirect
from post.models import Post
# Create your views here.


def post_list(request):
    return render(request, 'post_list.html', {})


def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(title=title, content=content)
        return redirect('/post/read/?post_id=%s' % post.id)
    return render(request, 'create_post.html', {})


def edit_post(request):
    if request.method == "POST":
        post_id = int(request.POST.get('post_id'))
        post = Post.objects.get(id=post_id)
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        post_id = request.GET.get('post_id')
        post = Post.objects.get(id=post_id)
        return render(request, 'edit_post.html', {'post': post})


def read_post(request):
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    return render(request, 'read_post.html', {'post': post})


def search_post(request):
    keyword = request.POST.get('keyword')

    postcc = Post.objects.filter(content__contains=keyword)

    return render(request, 'search_post.html', {'postcc': postcc})