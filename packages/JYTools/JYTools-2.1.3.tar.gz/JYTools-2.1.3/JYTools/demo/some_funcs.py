# !/usr/bin/env python
# coding: utf-8


__author__ = 'zhouhenglc'


def func_plus(a, b):
    print(a)
    print(b)
    return a + b


def func_multiplication(a, b):
    print(a)
    print(b)
    return a * b


def func_print_args(*args, **kwargs):
    print(args)
    print(kwargs)
