# !/usr/bin/env python
# coding: utf-8
from JYTools.JYWorker._func_task import FuncTaskGroup

from JYTools.demo import some_funcs

__author__ = 'zhouhenglc'


def test_ftg():
    ftg = FuncTaskGroup('test-ftg',
                        completed_func=some_funcs.func_print_args,
                        failed_func=some_funcs.func_print_args,
                        any_failed_func=some_funcs.func_print_args)
    ftg.add_sync_task(some_funcs.func_plus, '1', 5)
    ftg.add_sync_task(some_funcs.func_multiplication, 6, '5')
    ftg.start()


if __name__ == '__main__':
    test_ftg()
