from django.db import models

# Create your models here.


class User(models.Model):
    SEX = (
        ('M', '男性'),
        ('F', '女性'),
        ('U', '保密'),
    )
    nickname = models.CharField(max_length=32,unique=True)  # 多了不通知 直接截取掉
    password = models.CharField(max_length=128)
    icon = models.ImageField()
    age = models.IntegerField()
    sex = models.CharField(max_length=8, choices=SEX)