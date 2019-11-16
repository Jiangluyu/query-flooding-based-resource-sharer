#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = "thread.py"
__author__ = "louis"
__mtime__ = "2019/11/5"
"""
import threading
import connection
import config


class TcpServer(threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter

	def run(self):
		init_config = config.Config()
		peer = init_config.get_attr(self.threadID)

		peer_s = connection.Connection()
		peer_s.set_num(self.threadID)
		peer_s.set_ip(peer['ip_addr'])
		peer_s.set_server_port(peer['server_port'])
		peer_s.set_client_port(peer['client_port'])
		peer_s.set_share_dir(peer['share_dir'])
		peer_s.set_peer_list(peer['peer_list'])
		peer_s.update_peer_attr()
		peer_s.tcp_server()
