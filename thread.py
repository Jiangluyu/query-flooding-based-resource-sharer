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


class TcpServer(threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter

	def run(self):
		print("Starting" + self.name)
		init_config = config.Config()
		peer = init_config.get_attr(self.threadID)

		peer_s = connection.Connection()
		peer_s.set_num(self.threadID)
		peer_s.set_ip(peer['ip_addr'])
		peer_s.set_server_port(peer['server_port'])
		peer_s.set_client_port(peer['client_port'])
		peer_s.set_share_dir(peer['share_dir'])
		peer_s.set_peer_list(peer['peer_list'])
		peer_s.tcp_server()


class TcpClient(threading.Thread):
	def __init__(self, threadID, name, counter, destIP, dest_port, msg):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
		self.destIP = destIP
		self.dest_port = dest_port
		self.msg = msg

	def run(self):
		print("Starting" + self.name)
		init_config = config.Config()
		peer = init_config.get_attr(self.threadID)

		peer_c = connection.Connection()
		peer_c.set_ip(peer['ip_addr'])
		peer_c.set_server_port(peer['server_port'])
		peer_c.set_client_port(peer['client_port'])
		peer_c.set_share_dir(peer['share_dir'])
		peer_c.set_peer_list(peer['peer_list'])
		peer_c.update_peer_attr()
		peer_c.tcp_client_query(self.destIP, self.dest_port, self.msg)
