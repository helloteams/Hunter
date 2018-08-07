# coding: utf-8
from django.core.cache import cache

from common import rds
from post.models import Post


def page_cache(timeout):
    def wrapper1(func):
        def wrapper2(request):
            key = 'PageCache-%s-%s' % (request.session.session_key, request.get_full_path())
            response = cache.get(key)
            print('Get from cache', response)
            if response is None:
                response = func(request)
                print('Get from view', response)
                cache.set(key, response, timeout)
            return response

        return wrapper2

    return wrapper1


def read_count(read_view):
    def wrapper(request):
        post_id = int(request.GET.get('post_id'))
        rds.zincrby(name='ReadRank', value=post_id, amount=1)  # 阅读计数
        # rds.zincrby('ReadRank', post_id)
        return read_view(request)

    return wrapper


def get_top_n(num):  # 别写死 留有余地
    ''' 取出 Top N 的帖子及其阅读计数 '''
    # congredis取出原始数据
    ori_data = rds.zrevrange(b'ReadRank', 0, 9, withscores=True)
    '''ori_data = [(b'37', 89.0),
                 (b'40', 11.0),
                 (b'39', 10.0),
                 (b'38', 9.0),
                 (b'44', 2.0),
                 (b'36', 1.0),
                 (b'35', 1.0),
                 (b'20', 1.0),
                 (b'16', 1.0)]
    '''
    # 数据清洗
    cleaned_rank = [[int(post_id), int(count)] for post_id, count in ori_data]
    '''
    id_rank =
    [[37, 89],
     [40, 11],
     [39, 10],
     [38, 9],
     [44, 2],
     [36, 1],
     [35, 1],
     [20, 1],
     [16, 1]]
    '''

    # 思路一  效率极低
    '''
    for item in cleaned_rank:
        item[0] = Post.objects.get(id=item[0])
    rank_data = cleaned_rank
    return rank_data
    
    # for i in range(10):
    #     Post.objects.create()
    '''

    # 思路二  第一个为什么 逐个获取 改成批量获取 Post
    # 先取id
    # post_id_list = [ post_id for post_id,_ in cleaned_rank]
    # posts = Post.objects.filter(id__in=post_id_list)  # 批量发取出posts
    # posts = sorted(posts,key=lambda post: post_id_list.index(post.id))  # 调整为正确的顺序
    # rank_data = []
    # for post,(_, count) in zip(posts,cleaned_rank):
    #     rank_data.append([post, count])
    # return rank_data

    # 思路三
    post_id_list = [post_id for post_id, _ in cleaned_rank]

    post_dict = Post.objects.in_bulk((post_id_list))  # 批量获取 post 字典
    for item in cleaned_rank:
        post_id = item[0]
        item[0] = post_dict[post_id]

    rank_data = cleaned_rank
    return rank_data


# 先使用调试工具
# 先进行注释
# 理清思路
# 伪代码  表述思路
# 流程图
# 然后构造逻辑
