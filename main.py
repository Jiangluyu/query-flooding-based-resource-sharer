#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ""
__author__ = "louis"
__mtime__ = "2019/11/5"
"""

import config
import thread
import connection


if __name__ == '__main__':
    thread1 = thread.MYTHREAD(1, "THREAD1", 1)
    thread1.start()


    print("exit main thread")

