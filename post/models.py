from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

# 不建议
# for i in range(100):
#     Post.objects.create()


# for i in range(100):
#     Post.objects.bulk_create([...])


# User.objects.filter(id__lt=123).only('username', 'email')
# User.objects.filter(id__lt=123).defer('username', 'email')
# select username,email from