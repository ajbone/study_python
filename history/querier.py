#!/usr/bin/env python2.7

#coding:utf-8

import sys
import time
from PIL import Image
import base64
import shutil
import traceback
import threading
import subprocess


from xml.dom import minidom
from xml.dom.minidom import parseString
from subprocess import *

from amqper import *
from logger import *
from dbpc import dbpc


if len(sys.argv) != 3:
    print 'Usage: %s -f config' %sys.argv[0]
    sys.exit(0)

__filedir__ = os.path.dirname(os.path.abspath(__file__))
CONFIGFILE = sys.argv[2]

SourceHashTagName   = 'sourceUrlHash'
SourceTypeTagName   = 'category'
SourceSampleKey     = 'sampleKey'
MediaPathTagName    = 'sourceMediaPath'
DnaPathTagName      = 'sourceDnaPath'
SnapshotPathTagName = 'snapshot'
MatchMetaUUID       = 'metaUuid'
MatchMetaTitle      = 'metaTitle'
MatchOffset         = 'offsets'
MatchSampleOffset   = 'sampleOffset'
MatchRefOffset      = 'metaOffset'
MatchDuration       = 'matchDuration'
Thumbnail           = 'thumbnail'

QUERYTOOL = os.path.join(__filedir__, './tools/vdna_query/bin/vdna_query.py')

def ProcessDBPC(config):
    return dbpc(
            config.get('host', '192.168.1.146'),
            config.get('port', 5800),
            config.get('service', 'xhs'),
            config.get('component', 'querier'),
            config.get('interval', 120)
            )

def generateSubFolder(key):
    sub_folder = os.path.join(key[:2], key[-2:])
    return sub_folder

def setTaskTemplate(task):
    new_tasks = []
    results = task['result']
    del task['result']

    all_meta_uuid_str = ""
    for uuid in results.keys():
        dic = results[uuid]
        meta_uuid = dic['meta_uuid']
        all_meta_uuid_str += meta_uuid + "," 
    if all_meta_uuid_str and all_meta_uuid_str[-1] == ",":
        all_meta_uuid_str = all_meta_uuid_str[0:-1]

    task[SnapshotPathTagName] = all_meta_uuid_str
    for uuid in results.keys():
        dic = results[uuid]
        task[MatchMetaUUID]   = dic['meta_uuid']
        task[MatchMetaTitle]  = dic['meta_title']
        offsets = dic['offset']
        new_offset = []
        for o in offsets:
            new_dict = {}
            new_dict[MatchSampleOffset] = o['sample_offset']
            new_dict[MatchRefOffset]    = o['ref_offset']
            new_dict[MatchDuration]     = o['duration']
            new_dict[Thumbnail]         = o['thumbnail_path']
            new_offset.append(new_dict)

            task[Thumbnail]    = new_dict[Thumbnail]

        task[MatchOffset] = new_offset
        new_tasks.append(task)
    return new_tasks

class QueryWoker(object):
    def __init__(self, task, path_config, vddb_config, logger = None):
        self._task = task
        self._logger = logger
        self._path_config = path_config
        self._vddb_config = vddb_config

        self._sub_folder = None
        self._parseTask()
        self._parseConfig()
    
    def _parseTask(self):
        self._download_hash = self._task.get(SourceHashTagName)
        self._dna_file = self._task.get(DnaPathTagName, None)
        self._media_file = self._task.get(MediaPathTagName, None)
        self._source_type = self._task.get(SourceTypeTagName, 'image')
        if not self._source_type:
            self._source_type = 'image'
            self._task[SourceTypeTagName] = 'image'
    
    def _parseConfig(self):
        self._reject_score = int(self._vddb_config.get('reject_score'))
        self._dna_path = self._path_config.get('dna_path')
        self._media_path = self._path_config.get('media_path')
        self._thumbnail_path = self._path_config.get('thumbnail_path')

    def _checkImageType(self):
        if self._source_type == 'image':
            return True
        return False
    
    def _runCmdline(self, cmdline):
        p = subprocess.Popen(cmdline, stdout=PIPE, stderr=PIPE, shell=True)
        ret = p.wait()
        out, err = p.communicate()
        return ret, out, err

    def _queryVddb(self, dna_file):
        vdna_query_tool = os.path.join(__filedir__, './tools/vdna_query/bin/vdna_query')
        cmdline = '%s -s \'%s\' -u \'%s\' -w \'%s\' -i %s -TDNA' % (
            vdna_query_tool,
            self._vddb_config.get('server'),
            #str(vddb_config.get('port')),
            self._vddb_config.get('username'),
            self._vddb_config.get('password'),
            dna_file
        )

        if self._checkImageType():
            cmdline += ' --profile D'
        
        self._logger.info('query vddb cmdline [%s]' %cmdline)

        return self._runCmdline(cmdline)
    
    def _parseQueryResult(self, query_result):
        parseXML = lambda tag,num :\
                parseString(query_result).getElementsByTagName(tag)[num].firstChild.nodeValue

        ret_code = int(parseXML('return_code',0))
        ret_msg = parseXML('extra_info', 0)
        if ret_code != 0:
            return ret_code, msg

        result = {}
        size = parseString(query_result).getElementsByTagName('matches')[0].getAttribute('size')

        for i in range(int(size)):
            meta_uuid  = parseXML('master_uuid', i)
            meta_title = parseXML('master_name', i)
            track_type = parseXML('track_type', i)
            track_id   = parseXML('track_id', i)
            duration   = parseXML('match_duration', i)
            score      = parseXML('score', i)
            r_offset   = parseXML('reference_offset', i)
            s_offset   = parseXML('sample_offset', i)

            if int(track_id) != 0:
                self._logger.info('result track id is not 0, pass it...')
                continue

            if int(score) < self._reject_score:
                self._logger.info('result score[%s] less than %d, pass it' %(score, self._reject_score))
                continue
            
            if meta_uuid in result.keys():
                result_dict = {
                        'duration'     : int(duration),
                        'score'        : int(score),
                        'ref_offset'   : int(r_offset),
                        'sample_offset': int(s_offset)
                    }

                result[meta_uuid]['offset'].append(result_dict)
            else:
                result_dict = {
                    'meta_uuid'    : meta_uuid,
                    'meta_title'   : meta_title,
                    'track_type'   : track_type,
                    'track_id'     : int(track_id),
                    'offset'       : [
                        {
                            'duration'     : int(duration),
                            'score'        : int(score),
                            'ref_offset'   : int(r_offset),
                            'sample_offset': int(s_offset)
                            }
                        ]
                    }

                result[meta_uuid] = result_dict

        return ret_code, result

    def _genImageThumbnail(self, input_file, output_file):
        try:
            im = Image.open(input_file)
            w,h = im.size
            im_ss = im.resize((360, 240))
            im_ss.save(output_file)
        except Exception, msg:
            #raise Exception('resize image error[%s]' %msg)
            self._logger.error('resize image error[%s]' %msg)
    def _genVideoThumbnail(self, input_file, output_file, timestamp):
        ffmpeg_tool = os.path.join(__filedir__, './tools/ffmpeg')
        cmdline = '%s -i %s -y -ss %s -t %s -s 360*240 -f mjpeg -vframes 10 %s' %(
                    ffmpeg_tool,
                    input_file,
                    str(timestamp),
                    str(timestamp+1),
                    output_file
                )
        ret, out, err = self._runCmdline(cmdline)
        return os.path.getsize(output_file) if os.path.exists(output_file) else 0

    def getTask(self):
        return self._task

    def processTask(self):
        try:
            self._sub_folder = generateSubFolder(self._download_hash)
        except:
            self._logger.error('mkdir sub_folder err[%s]...' %(traceback.format_exc()))
        finally:
            return self._sub_folder

    def processQuery(self):
        if not self._dna_file:
            self._logger.error('no dna file to query')
            return

        dna_file = os.path.join(self._dna_path, self._dna_file)
        i = 0
        while True:
            ret, query_result, err = self._queryVddb(dna_file)
            if ret == 0:
                break
            
            i += 1
            if i == 3:
                self._logger.error('query vddb cost 3 times')
                self._logger.error('query vddb error[%s, %s]' %(query_result, err))
                break

        if ret != 0:
            raise Exception('query vddb error...')
            
        self._logger.debug('query vddb result %s' %(query_result))
        ret, result = self._parseQueryResult(query_result)

        if ret != 0:
            raise Exception('query vddb error[%s]' %str(msg))

        if not result:
            self._logger.info('no match...')

        self._task['result'] = result

    def processThumbnail(self):
        if not self._media_file:
            self._logger.error('no media file to get thumbnail')
            return

        media_file = os.path.join(self._media_path, self._media_file)
        thumbnail_relative_file = os.path.join(self._sub_folder, self._download_hash + '.jpg')
        thumbnail_file = os.path.join(self._thumbnail_path, thumbnail_relative_file)

        if not os.path.exists(os.path.dirname(thumbnail_file)):
            os.makedirs(os.path.dirname(thumbnail_file))

        result = self._task.get('result')
        if not result:
            return

        for uuid in result.keys():
            offset = result[uuid]['offset']
            new_offset = []

            for off in offset:
                if self._checkImageType():
                    self._genImageThumbnail(media_file, thumbnail_file)
                else:
                    s_offset = off['sample_offset']
                    duration = off['duration']
                    timestamp = (s_offset + duration) / 2
                    size = self._genVideoThumbnail(media_file, thumbnail_file, timestamp)

                off['thumbnail_path'] = thumbnail_relative_file
                new_offset.append(off)

                result[uuid]['offset'] = new_offset
        
        self._task['result'] = result

    def sendTaskToMQ(self, conn):
        if type(self._task) == type('123'):
            setTaskToMQ(conn, self._task)
            self._logger.debug('send to mq[%s]' %str(self._task))
            return

        if not self._task.get('result', None):
            if self._task.has_key('result'):
                del self._task['result']
            setTaskToMQ(conn, base64.b64encode(json.dumps(self._task)))
            self._logger.debug('send to mq[%s]' %str(self._task))
            self._logger.debug('send to base64 mq[%s]' %base64.b64encode(json.dumps(self._task)))
            return

        tasks = setTaskTemplate(self._task)
        for task in tasks:
            setTaskToMQ(conn, base64.b64encode(json.dumps(task)))
            self._logger.debug('send to mq[%s]' %str(task))
            self._logger.debug('send to base64 mq[%s]' %base64.b64encode(json.dumps(task)))

class Querier(object):
    def __init__(self):
        self._general_config = None
        self._dbpc_config = None
        self._vddb_config = None
        self._path_config = None
        self._loadConfig()

        self._loggers = {}
        self._amqers = {}

    def _loadConfig(self):
        config = json.loads(open(CONFIGFILE).read())
        self._general_config = config.get('general', None)
        self._dbpc_config = config.get('dbpc', None)
        self._vddb_config = config.get('vddb', None)
        self._path_config = config.get('path', None)
        self._mq_config = config.get('mq', None)
        self._log_config = config.get('logger', None)

    def checkConfig(self):
        if self._general_config and self._dbpc_config\
                and self._vddb_config and self._path_config\
                and self._mq_config and self._log_config:
            return True
        return False

    def _getLogger(self, name):
        logger = Logger()
        logger.init_logger(
            self._log_config.get('module') + '-' + name,
            self._log_config.get('level'),
            self._log_config.get('file'),
            SysLogHandler.LOG_LOCAL1
        )
        return logger
    
    def _getMqer(self, logger):
        conn = amqper(
            self._mq_config.get('server'), 
            self._mq_config.get('exchange'),
            self._mq_config.get('routing_key'),
            self._mq_config.get('request_queue'),
            self._mq_config.get('response_queue'),
            None,
            logger
            )
        return conn

    def _worker(self, name):
        logger = self._loggers[name]
        mqConn = self._amqers[name]
        logger.info('Thread[%s] start...  connect mq successfully...' %(name))
        logger.info('Thread[%s] wait for task..' %(name))
        while True:
            try:
                task = getTaskFromMQ(mqConn)
                if task == None:
                    #logger.debug('task is none, re get task after sleep one second...')
                    time.sleep (1)
                    continue

                logger.debug ('task is %s' %str(task))
                task = json.loads(base64.b64decode(task))
                logger.debug ('after decode, task is %s' %str(task))
            except:
                logger.error('get task from mq err, get task is %s' %str(task))
                logger.error('traceback.errmsg: %s' %traceback.format_exc())
                continue
            try:
                worker = QueryWoker(task, self._path_config, self._vddb_config, logger)
            except:
                logger.error('gen QueryWoker error...')
                logger.error('traceback.errmsg: %s' %traceback.format_exc())
                continue

            try:
                worker.processTask()
                worker.processQuery()
                worker.processThumbnail()

            except Exception, msg:
                logger.error('error msg: %s, traceback.errmsg: %s' %(str(msg), traceback.format_exc()))
            finally:
                worker.sendTaskToMQ(mqConn)

    def run(self):
        if not self.checkConfig():
            raise Exception('load config err...')

        dbpc_th = ProcessDBPC(self._dbpc_config)
        dbpc_th.start()

        process_num = self._general_config.get('process_num')
        worker_ths = []
        for i in range(process_num):
            threadName = 'Thread' + str(i+1)
            self._loggers[threadName] = self._getLogger(threadName)
            self._amqers[threadName] = self._getMqer(self._loggers[threadName])
            worker_th = threading.Thread(target=self._worker, args=(threadName,))
            worker_ths.append(worker_th)

        for worker_th in worker_ths:
            #worker_th.setDaemon(True)
            worker_th.start()

def main():
    querier = Querier()
    querier.run()

if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc()
