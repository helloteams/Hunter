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

    def roles(self):
        ''' 用户所绑定的所有角色  '''
        # 通过关系表筛选关联的 所言 role_id
        relations = UserRoleRelation.objects.filter(uid=self.id).only('role_id')
        role_id_list = [r.role_id for r in relations]

        return Role.objects.filter(id__in=role_id_list)

    def has_perm(self, perm_name):
        # need_perm = Permission.objects.get(name=perm_name)
        # return self.perm.level >= need_perm.level
        for role in self.roles():
            for perm in role.perms():
                if perm.name == perm_name:
                    return True
        return False


class UserRoleRelation(models.Model):  # 先列出關系表
    uid = models.IntegerField()
    role_id = models.IntegerField()

    @classmethod
    def add_role_to_user(cls, uid, role_name):
        role = Role.objects.get(name=role_name)
        return cls.objects.create(uid=uid, role_id=role.id)

    @classmethod
    def del_role_from_user(cls, uid, role_name):
        role = Role.objects.get(name=role_name)
        cls.objects.get(uid=uid, role_id=role.id).delete()


'''
    第一次簡單的權限設計:
    perm_id = models.IntegerField()

    @property
    def perm(self):
        if not hasattr(self, '_perm'):
            self._perm = Permission.objects.get(id=self.perm_id)
        return self._perm

    def has_perm(self, perm_name):
        need_perm = Permission.objects.get(name=perm_name)
        return self.perm.level >= need_perm.level
'''


# 基於等級
class Role(models.Model):
    '''
    角色表:
    admin  管理員
    manager 斑竹
    user    普通用戶


    '''
    name = models.CharField(max_length=16, unique=True)

    def perms(self):
        # 角色绑定的所有权限
        # 通过关系表筛选关联的 perm_id
        relations = RolePermRelation.objects.filter(role_id=self.id).only('perm_id')
        perm_id_list = [r.perm_id for r in relations]
        return Permission.objects.filter(id__in=perm_id_list)


class RolePermRelation(models.Model):
    role_id = models.IntegerField()
    perm_id = models.IntegerField()

    @classmethod
    def add_perm_to_role(cls, role_id, perm_name):
        '''给角色添加权限'''
        perm = Permission.objects.get(name=perm_name)
        return cls.objects.create(role_id=role_id, perm_id=perm.id)

    @classmethod
    def del_perm_from_role(cls, role_id, perm_name):
        '''删除角色绑定的一个权限'''
        perm = Permission.objects.get(name=perm_name)
        cls.objects.get(role_id=role_id, perm_id=perm.id).delete()


class Permission(models.Model):
    # level = models.IntegerField()
    '''
    權限表:
    add_post 發表帖子
    del_post 刪除帖子
    add_comment 發表評論
    del_comment 刪除評論
    del_user 刪除用戶
    '''
    name = models.CharField(max_length=16, unique=True)


'''
In [1]: from user.models import User,Role,Permission,UserRoleRelation,RolePermRelation

In [2]: perms = [Permission(name='add_post'),Permission(name='del_post'),Permission(name='add_comment'),Permission(name='del_comment'),Permission(name='del_user')]

In [3]: Permission.objects.bulk_create(perms)
Out[3]: 
[<Permission: Permission object>,
 <Permission: Permission object>,
 <Permission: Permission object>,
 <Permission: Permission object>,
 <Permission: Permission object>]
 
In [2]: Role
Out[2]: user.models.Role

In [3]: Role.objects.bulk_create([Role(name='admin'),Role(name='manager'),Role(name='user')])
Out[3]: [<Role: Role object>, <Role: Role object>, <Role: Role object>]

In [4]: User.objects.all()
Out[4]: <QuerySet [<User: User object>, <User: User object>, <User: User object>, <User: User object>, <User: User object>]>

In [5]: for u in User.objects.all():
   ...:     print(u.id,u.nickname)
   ...:     
1 adu
2 adu1
3 adu3
4 adudu
888 未登录

In [6]: adu3 = User.objects.get(nickname='adu3')

In [7]: adu3
Out[7]: <User: User object>

In [8]: adu3.id
Out[8]: 3

In [9]: adu3.nickname
Out[9]: 'adu3'

In [10]: adu1 = User.objects.get(nickname='adu1')

In [11]: adu = User.objects.get(nickname='adu')

In [12]: adu.id
Out[12]: 1

In [10]: RolePermRelation.add_perm_to_role(admin.id,'del_user')
Out[10]: <RolePermRelation: RolePermRelation object>

In [11]: RolePermRelation.add_perm_to_role(admin.id,'del_post')
Out[11]: <RolePermRelation: RolePermRelation object>

In [12]: RolePermRelation.add_perm_to_role(admin.id,'del_comment')
Out[12]: <RolePermRelation: RolePermRelation object>

In [13]: RolePermRelation.add_perm_to_role(manager.id,'del_comment')
Out[13]: <RolePermRelation: RolePermRelation object>

In [14]: RolePermRelation.add_perm_to_role(manager.id,'del_post')
Out[14]: <RolePermRelation: RolePermRelation object>

In [16]: RolePermRelation.add_perm_to_role(manager.id,'add_comment')
Out[16]: <RolePermRelation: RolePermRelation object>

In [17]: RolePermRelation.add_perm_to_role(user.id,'add_comment')
Out[17]: <RolePermRelation: RolePermRelation object>

In [18]: RolePermRelation.add_perm_to_role(user.id,'add_post')
Out[18]: <RolePermRelation: RolePermRelation object>



'''