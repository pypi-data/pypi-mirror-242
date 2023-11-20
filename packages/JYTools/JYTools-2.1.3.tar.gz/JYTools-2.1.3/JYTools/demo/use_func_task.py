# !/usr/bin/env python
# coding: utf-8
from JYTools.demo import some_funcs
from JYTools.JYWorker import RedisQueue
from JYTools.JYWorker._func_task import run_fun_task

__author__ = 'zhouhenglc'

redis_queue = RedisQueue()
run_fun_task(redis_queue, '1234', some_funcs.func_plus, 1, 2)
