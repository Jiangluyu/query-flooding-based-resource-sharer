#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ""
__author__ = "louis"
__mtime__ = "2019/11/5"
"""
import threading
import connection
import config


class MYTHREAD(threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter

	def run(self):
		print("Starting" + self.name)
		init_config = config.Config()
		peer_2 = init_config.get_attr(2)

		peer_s = connection.Connection()
		peer_s.set_ip(peer_2['ip_addr'])
		peer_s.set_server_port(peer_2['server_port'])
		peer_s.set_client_port(peer_2['client_port'])
		peer_s.set_share_dir(peer_2['share_dir'])
		peer_s.set_peer_list(peer_2['peer_list'])
		peer_s.tcp_server()
