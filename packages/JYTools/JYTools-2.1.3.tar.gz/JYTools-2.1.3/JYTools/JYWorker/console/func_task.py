# !/usr/bin/env python
# coding: utf-8
from JYTools.JYWorker.function import FuncTaskWorker
from JYTools.JYWorker import worker_run


__author__ = 'zhouhenglc'


def run_func_task_worker():
    worker_run(FuncTaskWorker)


def run():
    run_func_task_worker()


if __name__ == '__main__':
    run()
