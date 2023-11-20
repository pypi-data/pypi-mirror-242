#! /usr/bin/env python
# coding: utf-8
import sys

from setuptools import setup


if sys.version_info <= (3, 5):
    sys.stderr.write("ERROR: jingyun tools requires Python Version 3.6 or above.\n")
    sys.stderr.write("Your Python Version is %s.%s.%s.\n" % sys.version_info[:3])
    sys.exit(1)

setup()
