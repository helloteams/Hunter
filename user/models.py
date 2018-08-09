from django.db import models


# Create your models here.


class User(models.Model):
    SEX = (
        ('M', '男性'),
        ('F', '女性'),
        ('U', '保密'),
    )
    nickname = models.CharField(max_length=32, unique=True)  # 多了不通知 直接截取掉
    password = models.CharField(max_length=128)
    icon = models.ImageField()
    age = models.IntegerField()
    sex = models.CharField(max_length=8, choices=SEX)

    perm_id = models.IntegerField()

    @property
    def perm(self):
        if not hasattr(self, '_perm'):
            self._perm = Permission.objects.get(id=self.perm_id)
        return self._perm

    def has_perm(self, perm_name):
        need_perm = Permission.objects.get(name=perm_name)
        return self.perm.level >= need_perm.level


class Permission(models.Model):
    level = models.IntegerField()
    name = models.CharField(max_length=16, unique=True)
