from django.db import models

# Create your models here.
from user.models import User


class Post(models.Model):
    uid = models.IntegerField()
    title = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    @property  # 属性
    def auth(self):
        if not hasattr(self, '_auth'):
            self._auth = User.objects.get(id=self.uid)
        return self._auth

    def comments(self):
        return Comment.objects.filter(post_id=self.id).order_by('-id')

    def tags(self):
        relations = PostTagRelation.objects.filter(post_id=self.id).only('tag_id')
        tag_id_list = [r.tag_id for r in relations]
        return Tag.objects.filter(id__in=tag_id_list)

    def update_tags(self, tag_names):
        Tag.ensure_tags(tag_names)
        update_names = set(tag_names)
        exist_names = {t.name for t in self.tags()}
        # 筛选出新创建的关系
        need_create_names = update_names - exist_names
        PostTagRelation.add_post_tags(self.id, need_create_names)

        # 筛选出需要删除的关系
        need_delete_names = exist_names - update_names
        PostTagRelation.del_post_tags(self.id, need_delete_names)


class Comment(models.Model):
    uid = models.IntegerField()
    post_id = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def auth(self):
        if not hasattr(self, '_auth'):
            self._auth = User.objects.get(id=self.uid)
        return self._auth

    def post(self):
        if not hasattr(self, '_post'):
            self._post = Post.objects.get(id=self.post_id)
        return self._post


class Tag(models.Model):
    name = models.CharField(max_length=16, unique=True)

    @classmethod
    def ensure_tags(cls, tag_names):
        '''确保传入的 那么 存在 '''
        tags = cls.objects.filter(name__in=tag_names).only('name')
        exist_names = {t.name for t in tags}  # [t.name for t in tags]
        new_names = set(tag_names) - exist_names
        need_create = [cls(name=name) for name in new_names]
        cls.objects.bulk_create(need_create)
        # need_create = [cls(name=name)
        #                for name in tag_names
        #                if name not in exist_names]

    def posts(self):
        relations = PostTagRelation.objects.filter(tag_id=self.id).only('post_id')
        post_id_list = [r.post_id for r in relations]
        return Post.objects.filter(id__in=post_id_list)


class PostTagRelation(models.Model):
    post_id = models.IntegerField()
    tag_id = models.IntegerField()

    @classmethod
    def add_post_tags(cls, post_id, tag_names):
        tag_id_list = [t.id for t in Tag.objects.filter(name__in=tag_names)]
        relations = [cls(post_id=post_id, tag_id=tid)for tid in tag_id_list]
        cls.objects.bulk_create(relations)

    @classmethod
    def del_post_tags(cls, post_id, tag_names):
        tag_id_list = [t.id for t in Tag.objects.filter(name__in=tag_names)]
        cls.objects.filter(post_id=post_id, tag_id__in=tag_id_list).delete()

# # 不建议
# # for i in range(100):
# #     Post.objects.create()
#
#
# # for i in range(100):
# #     Post.objects.bulk_create([...])
#
# # User.objects.filter(id__lt=123).only('username', 'email')
# # User.objects.filter(id__lt=123).defer('username', 'email')
# # select username,email from


# class Tag(models.Model):
#     name = models.CharField(max_length=16, unique=True)
#
# # Python编码风格  python  codestyle
# # Django部署      python  django     linux
# # Nginx开发       python  django     linux
