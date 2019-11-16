#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = "main.py                                                                                                                                                            "
__author__ = "louis"
__mtime__ = "2019/11/5"
"""

import thread
import config
import connection
import time


def get(role_num, filename):
    init_config = config.Config()
    peer = init_config.get_attr(role_num)
    peer_c = connection.Connection()
    peer_c.set_ip(peer['ip_addr'])
    peer_c.set_server_port(peer['server_port'])
    peer_c.set_client_port(peer['client_port'])
    peer_c.set_share_dir(peer['share_dir'])
    peer_c.set_peer_list(peer['peer_list'])
    peer_attr = peer_c.update_peer_attr()
    for i in peer_attr:
        peer_c.tcp_client_notice(i['ip_addr'], i['server_port'], "get %s %s %s %s" % (
            opt.split()[1], peer['server_port'], peer['ip_addr'], init_config.get_ttl()))
    time.sleep(3)
    if peer_c.get_timeout_flag()[filename] == 1:
        print("timeout")


if __name__ == '__main__':
    peer_num = config.Config().get_peer_num()
    for i in range(peer_num):
        exec('thread{} = thread.TcpServer(i, "THREAD%s" % i, i)'.format(i, i))
        exec('thread{}.start()'.format(i))

    print("flood-query-system v1.0 by louis")
    while True:
        print()
        print('**********************************')
        role = int(input("input peer num:"))
        opt = input("input opt:")
        print()
        if opt.split()[0] == 'get':
            get(role, opt.split()[1])
        elif opt.split()[0] == 'config':
            with open("config.ini", 'r') as f:
                line_num = 0
                while True:
                    line = f.readline()
                    line_num += 1
                    if 7*role <= line_num <= 7*role + 6:
                        print(line, end="")
                    if not line:
                        break
        elif opt.split()[0] == 'exit':
            exit()

