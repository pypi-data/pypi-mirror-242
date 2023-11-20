#! /usr/bin/env python
# coding: utf-8

import sys
import logging
from ._redis import RedisWorker, RedisQueue, RedisStat
from ._Worker import ReadWorkerLog
from ._async import AsyncRedisWorker, AsyncStatRedisWorker
from ._Task import TaskStatus, TaskType
from ._du import DAGWorker, DAGTools
from .UploadLog import UploadLogWorker

__author__ = 'meisanggou'


logging.basicConfig(level=logging.INFO, format="%(message)s")


def worker_run(worker_class, default_work_tag=None, argv=None):
    if issubclass(worker_class, RedisWorker) is False:
        print("Error worker class")
        return 1, None
    if issubclass(worker_class, RedisWorker) is True:
        args = worker_class.parse_args(argv)
        if args.sys_paths:
            for path in args.sys_paths:
                sys.path.append(path)
        if args.debug is True:
            logging.basicConfig(level=logging.DEBUG)
        if args.work_tag is None:
            args.work_tag = default_work_tag
        app = worker_class(
            conf_path=args.conf_path, heartbeat_value=args.heartbeat_value,
            work_tag=args.work_tag, log_dir=args.log_dir)
        if args.example_path is not None:
            o = app.test(key=args.key, params_path=args.example_path,
                         sub_key=args.sub_key, report_tag=args.report_tag,
                         report_scene=args.report_scene)
            return 0, o
        else:
            app.work(args.daemon)
    return 0, None
