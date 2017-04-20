#!/usr/bin/env python
# coding: utf-8
import sys
import traceback
import json

from etc import config as cf
from com_logger import logger
from com_amqp import Amqp
from utils import (DownloadFailException, TokenExpiresException,
                   ParameterException, FetchArticleException,
                   LineNotConfigException, SaveMysqlRetryException,
                   NoDocIdException, HTTPConnectException)
from fetch_article import FetchArticle
from downloader import Downloader
from mysql_access import AccessMysql
from manager import ingest
reload(sys)
sys.setdefaultencoding('utf-8')


def run():
    def process_task(tasks, message):
        def parse_one_task(task):
            def add_out_retry():
                mysql_db.down_fail(doc_lib_id, doc_id, mysql_db.out_type, 1)

            try:
                doc_id = str(task[ld[0]])
                doc_lib_id = str(task[ld[1]])
                main_log = '{}: {}, {}: {}, {}: {}, {}: {}'.format(
                    ld[0], doc_id, ld[1], doc_lib_id, ld[2], task[ld[2]],
                    ld[3], task[ld[3]])
            except:
                logger.error('task:[{}], can not found [{}], {}'.format(
                    str(task), ld, traceback.format_exc()))
            else:
                try:
                    logger.message_decorate(main=main_log)
                    bAdd = True
                    if 'add' == task[ld[3]]:
                        if 6 == task[ld[1]]:
                            bAdd = False
                            logger.warn('drop task, not add 6 报刊')
                    else:
                        bAdd = False
                        logger.warn('drop task, not add type, {}'.format(task))
                    if bAdd:
                        article_info = article_obj.fetch(doc_id, doc_lib_id)
                        if 'fetch_error' in article_info:
                            raise FetchArticleException()
                        elif 'not_in_config_error' in article_info:
                            raise LineNotConfigException(
                                article_info['not_in_config_error'])
                        else:
                            ingest(mysql_db, download_obj, article_info, 1)
                except TokenExpiresException:
                    add_out_retry()
                except DownloadFailException, e:
                    logger.warn(str(e))
                    add_out_retry()
                except (ParameterException, HTTPConnectException), e:
                    try:
                        j = json.loads(str(e))
                        logger.error(j)
                    except:
                        logger.error(str(e))
                    add_out_retry()
                except FetchArticleException:
                    logger.error(article_info)
                    if 'message' in article_info:
                        if '系统异常，请联系相关负责人' in article_info['message']:
                            logger.error('ack this task (系统异常，请联系相关负责人)')
                        else:
                            add_out_retry()
                    else:
                        add_out_retry()
                except NoDocIdException:
                    logger.error(article_info)
                except LineNotConfigException, e:
                    logger.warn(str(e))
                except SaveMysqlRetryException, e:
                    try:
                        j = json.loads(str(e))
                        logger.warn(j)
                    except:
                        logger.warn(str(e))
                except:
                    logger.error(traceback.format_exc())
                    add_out_retry()
                finally:
                    logger.message_undecorate()

        if not tasks:
            logger.warn('receive empty task')
            message.ack()
            return
        else:
            try:
                eval(tasks)
            except:
                logger.error('tasks:[{}], {}'.format(
                    str(tasks), traceback.format_exc()))
                message.ack()
                return
        ld = ('doc_id', 'doc_lib_id', 'create_date', 'type')
        obj_tasks = eval(tasks)
        if isinstance(obj_tasks, list):
            logger.info('get tasks is list, len = {}'.format(len(obj_tasks)))
            for task in obj_tasks:
                logger.info('parse one task, [{}]'.format(task))
                parse_one_task(task)
        elif isinstance(obj_tasks, dict):
            logger.info('get tasks is dict, [{}]'.format(obj_tasks))
            parse_one_task(obj_tasks)
        else:
            logger.error('unkonw task type, [{}], [{}]'.format(
                type(obj_tasks), obj_tasks))
        message.ack()

    mysql_db = AccessMysql(cf.db_url)
    article_obj = FetchArticle(mysql_db)
    article_obj.load_product()
    download_obj = Downloader()
    with Amqp(cf.download_queue_url, cf.download_exchange,
              cf.download_queue_name, cf.download_routing_key) as q:
        q.poll(process_task)


def main():
    try:
        logger.info('ingest start')
        run()
    except:
        logger.error(traceback.format_exc())


if __name__ == '__main__':
    main()
