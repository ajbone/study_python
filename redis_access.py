#!/usr/bin/env python
# encoding: utf-8
import redis
# from redis import ConnectionError, ReadOnlyError


class AccessRedis(object):
    def __init__(self, redis_url):
        self.redis_url = redis_url

    def connect(self):
        self._redis = redis.from_url(self.redis_url, retry_on_timeout=True)

    def insert_catch(self, url, title, md5):
        self._redis.set(md5, url + '$$$' + title)

    def get_catch_num(self, md5):
        if self._redis.exists(md5):
            return True
        else:
            return None


def test():
    access = AccessRedis("redis://120.26.52.123:6379/6")
    access.connect()
    c = access.get_catch_num('abc')


if __name__ == '__main__':
    import traceback
    try:
        test()
    except:
        print traceback.format_exc()
