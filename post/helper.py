# coding: utf-8
from django.core.cache import cache


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
