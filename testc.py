#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = "testc.py"
__author__ = "louis"
__mtime__ = "2019/11/5"
"""
import config
import connection
import time

init_config = config.Config()
peer_1 = init_config.get_attr(1)
peer_c = connection.Connection()
peer_c.set_ip(peer_1['ip_addr'])
peer_c.set_server_port(peer_1['server_port'])
peer_c.set_client_port(peer_1['client_port'])
peer_c.set_share_dir(peer_1['share_dir'])
peer_c.set_peer_list(peer_1['peer_list'])
peer_attr = peer_c.update_peer_attr()
file = input("input filename\n")
for i in peer_attr:
	peer_c.tcp_client_notice(i['ip_addr'], i['server_port'], "get %s %s %s %s" % (file, peer_1['server_port'], peer_1['ip_addr'], init_config.get_ttl()))
time.sleep(3)
if peer_c.get_timeout_flag()[file] == 1:
	print("timeout")

peer_3 = init_config.get_attr(5)
peer_d = connection.Connection()
peer_d.set_ip(peer_3['ip_addr'])
peer_d.set_server_port(peer_3['server_port'])
peer_d.set_client_port(peer_3['client_port'])
peer_d.set_share_dir(peer_3['share_dir'])
peer_d.set_peer_list(peer_3['peer_list'])
peer_attrs = peer_d.update_peer_attr()
file2 = input("input filename2\n")
for i in peer_attrs:
	peer_d.tcp_client_notice(i['ip_addr'], i['server_port'], "get %s %s %s %s " % (file2, peer_3['server_port'], peer_3['ip_addr'], init_config.get_ttl()))