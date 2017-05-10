/#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import time
from etc import config as cf
from functools import partial
import hashlib
import urllib
from DBUtils.PersistentDB import PersistentDB
import MySQLdb
from com_logger import logger

reload(sys)
sys.setdefaultencoding('utf-8')

ERROR_TYPE_BUSY = -1  # 系统繁忙，此时请开发者稍候再试
ERROR_TYPE_TOKEN = -2  # access_token已过期
ERROR_TYPE_NO_ATTACHE = -3  # 找不到附件


class XMLParseException(Exception):
    pass


class XMLDownException(Exception):
    pass


class XML2SmallException(Exception):
    pass


class MetaDownException(Exception):
    pass


class MetaIngestException(Exception):
    pass


class MetaNotExistsException(Exception):
    pass


class ImgSmallEnoughException(Exception):
    pass


class DownloadFailException(Exception):
    pass


class TokenExpiresException(Exception):
    pass


class ParameterException(Exception):
    pass


class FetchArticleException(Exception):
    pass


class LineNotConfigException(Exception):
    pass


class SaveMysqlRetryException(Exception):
    pass


class NoDocIdException(Exception):
    pass


class DataServerBusyException(Exception):
    pass


class HTTPConnectException(Exception):
    pass


def cur_file_dir():
    # 获取脚本文件的当前路径
    path = sys.path[0]
    # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


class Retry(object):
    default_exceptions = (Exception)

    def __init__(self, tries, exceptions=None, delay=0):
        """
        Decorator for retrying function if exception occurs
        tries -- num tries
        exceptions -- exceptions to catch
        delay -- wait between retries
        """
        self.tries = tries
        if exceptions is None:
            exceptions = Retry.default_exceptions
        self.exceptions = exceptions
        self.delay = delay

    def __call__(self, f):
        def fn(*args, **kwargs):
            exception = self.exceptions
            for i in range(self.tries):
                try:
                    return f(*args, **kwargs)
                except self.exceptions, e:
                    if (i + 1) < self.tries:
                        time.sleep(self.delay)
                    logger.error(str(e))
                    exception = e
            # if no success after tries, raise last exception
            raise exception
        return fn


def tn(name):
    if name in cf.video_types:
        return 'video'
    elif name in cf.image_types:
        return 'image'
    elif name in cf.text_types:
        return 'text'


def get_file_size(local_path):
    if os.access(local_path, os.R_OK):
        return os.stat(local_path).st_size
    return 0


def get_md5_value(src):
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest


def get_md5(media_file):
    m2 = hashlib.md5()
    m2.update(open(media_file).read())
    return m2.hexdigest()


def parse_url(url, default_port=None):
    '''
    Parse url in the following form:
      PROTO://[USER:[:PASSWD]@]HOST[:PORT][/PATH[;ATTR][?QUERY]]
    A tuple containing (proto, user, passwd, host, port,
        path, tag, attrs, query) is returned,
    where `attrs' is a tuple containing ('attr1=value1', 'attr2=value2', ...)
    '''
    proto, user, passwd, host, port, path, tag, attrs, query = (None, ) * 9

    try:
        proto, tmp_host = urllib.splittype(url)
        tmp_host, tmp_path = urllib.splithost(tmp_host)
        tmp_user, tmp_host = urllib.splituser(tmp_host)
        if tmp_user:
            user, passwd = urllib.splitpasswd(tmp_user)
        host, port = urllib.splitport(tmp_host)
        port = int(port) if port else default_port
        tmp_path, query = urllib.splitquery(tmp_path)
        tmp_path, attrs = urllib.splitattr(tmp_path)
        path, tag = urllib.splittag(tmp_path)
    except Exception, err:
        raise Exception('parse_db_url error - {0}'.format(str(err)))

    return proto, user, passwd, host, port, path, tag, attrs, query


def parse_db_url(db_url, default_port=None):
    '''
    Parse an url representation of one database settings.
    The `db_url' is in the following form:
      PROTO://[USER[:PASSWD]@]HOST[:PORT][/DB/TABLE]
    Tuple (proto, user, passwd, host, port, db, table) is returned
    '''
    proto, user, passwd, host, port, db, table = (None, ) * 7

    try:
        proto, user, passwd, host, port, path = parse_url(db_url,
                                                          default_port)[0:6]
        if not passwd:
            passwd = ''
        tmp_list = path.split('/')[1:]
        db, table = '', ''
        if len(tmp_list) >= 2:
            db, table = tmp_list[0:2]
        elif len(tmp_list) == 1:
            db = tmp_list[0]
    except Exception, err:
        raise Exception('parse_db_url error - {0}'.format(str(err)))

    return proto, str(user), str(passwd), str(host), port, str(db), str(table)


def make_conn(db_url, *args, **kwargs):
    _, user, passwd, host, port, db, _ = parse_db_url(db_url)
    conn = MySQLdb.connect(host=host,
                           port=port,
                           user=user,
                           passwd=passwd,
                           db=db,
                           charset='utf8',
                           use_unicode=False)
    # cur = conn.cursor()
    # cur.execute('set time_zone="+0:00"')
    # cur.close()
    # conn.commit()
    return conn


def make_pool(db_url):
    return PersistentDB(creator=partial(make_conn, db_url))


def get_error_type(source):
    if isinstance(source, dict):
        if 'resultmsg' in source:
            if '系统繁忙，此时请开发者稍候再试' in source['resultmsg']:
                return ERROR_TYPE_BUSY
            elif 'access_token已过期' in source['resultmsg']:
                return ERROR_TYPE_TOKEN
        elif 'resultcode' in source:
            if '系统繁忙，此时请开发者稍候再试' in source['resultcode']:
                return ERROR_TYPE_BUSY
        elif 'message' in source:
            if '找不到附件' in source['message']:
                return ERROR_TYPE_NO_ATTACHE
    else:
        logger.error('source is not dict, [{}]'.format(source))


g_retry_types = ['Photo', 'Video', 'VDDB', 'TDDB', 'BUSY', 'OUT']


def retry_info(fetch_type, mysql_db):
    meta_type = None
    max_retry_num = None
    sleep_seconds = None
    if fetch_type == 'Photo':
        meta_type = mysql_db.img_type
        max_retry_num = cf.photo_fail_max_retry
        sleep_seconds = min(cf.photo_fail_interval_sec, 10)
    elif fetch_type == 'Video':
        meta_type = mysql_db.video_type
        max_retry_num = cf.video_fail_max_retry
        sleep_seconds = min(cf.video_fail_interval_sec, 10)
    elif fetch_type == 'VDDB':
        meta_type = mysql_db.vddb_type
        max_retry_num = cf.vddb_fail_max_retry
        sleep_seconds = min(cf.vddb_fail_interval_sec, 10)
    elif fetch_type == 'TDDB':
        meta_type = mysql_db.tddb_type
        max_retry_num = cf.tddb_fail_max_retry
        sleep_seconds = min(cf.tddb_fail_interval_sec, 10)
    elif fetch_type == 'BUSY':
        meta_type = mysql_db.busy_type
        max_retry_num = cf.service_busy_max_retry
        sleep_seconds = min(cf.service_busy_interval_sec, 10)
    elif fetch_type == 'OUT':
        meta_type = mysql_db.out_type
        max_retry_num = cf.out_exception_fail_max_retry
        sleep_seconds = min(cf.out_exception_fail_interval_sec, 10)
    else:
        logger.error('get retry_info, unkown type [{}]'.format(fetch_type))
    return meta_type, max_retry_num, sleep_seconds


if __name__ == '__main__':
    # img_path = r'./var/XxjpsgC000003_20161024_TPPFN1A001.jpg'
    # resize_img(img_path, None)
    assert(ERROR_TYPE_BUSY == get_error_type({"resultcode": "系统繁忙，此时请开发者稍候再试!"}))
    assert(ERROR_TYPE_BUSY == get_error_type({"resultmsg":"系统繁忙，此时请开发者稍候再试!!!","resultcode":"3500"}))
    assert(ERROR_TYPE_TOKEN == get_error_type({"resultmsg":"access_token已过期","resultcode":"3500"}))
    pass
