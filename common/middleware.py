import time

from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache


# class MiddlewareMixin(object):
#     def __init__(self, get_response=None):
#         self.get_response = get_response
#         super(MiddlewareMixin, self).__init__()
#
#     def __call__(self, request):
#         response = None
#         if hasattr(self, 'process_request'):
#             response = self.process_request(request)
#         if not response:
#             response = self.get_response(request)
#         if hasattr(self, 'process_response'):
#             response = self.process_response(request, response)
#         return response


def simple_middleware(view_func):
    def middleware(request):
        print('exec-->process_request')
        response = view_func(request)  # views 函数在这里执行
        print('exec-->process_response')
        return response

    return middleware


class BlockMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # user_ok = request.META
        # print('---------------------------------')
        # print(user_ok)
        # print('---------------------------------')

        # 取出用户 Ip,并设置相关的key
        user_ip = request.META['REMOTE_ADDR']
        reqeust_key = 'RequestTime-%s' % user_ip
        block_key = 'Blocker-%s' % user_ip

        # 检查用户是否被封禁 cahche
        if cache.get(block_key):
            return render(request, 'blockers.html')

        # 取出当前时间和历史访问时间
        now = time.time()
        request_log = cache.get(reqeust_key, [0, 0, 0])
        t0, t1, t2 = request_log

        if (now - t0) < 1:
            # 封禁ip
            cache.set(block_key, 1, 15)
            return render(request, 'blockers.html')
        else:
            # 更新访问时间
            cache.set(reqeust_key, [t1, t2, now])

    # def process_response(self, request, response):
    #     pass

# 时间戳
# time.time()
# 1533623904.4799902

# time.time() 2
# 1533623972.345527
