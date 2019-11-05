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
    thread0 = thread.TcpServer(0, "THREAD0", 0)
    thread0.start()

    thread1 = thread.TcpServer(2, "THREAD2", 2)
    thread1.start()

    thread2 = thread.TcpServer(3, "THREAD3", 3)
    thread2.start()

    thread3 = thread.TcpServer(4, "THREAD4", 4)
    thread3.start()



