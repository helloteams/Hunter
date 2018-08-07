from django.conf import settings
from redis import Redis

# rds = Redis('127.0.0.1', 6379, db=1)
rds = Redis(**settings.REDIS)  # 床架你全局的REDIS连接实例
