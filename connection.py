#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ""
__author__ = "louis"
__mtime__ = "2019/11/5"
"""
import socket
import glob
import os
import struct
import json


class Connection:
	# 自身属性
	__ip_addr = None
	__server_port = None
	__client_port = None
	__peer_list = None
	__share_dir = None

	__addr = None

	# 服务器端收到的命令
	__s_cmd = []
	__c_cmd = []
	__source_ip_addr = None
	__source_port = None

	def set_ip(self, ip_addr):
		self.__ip_addr = ip_addr

	def set_server_port(self, server_port):
		self.__server_port = int(server_port)

	def set_client_port(self, client_port):
		self.__client_port = int(client_port)

	def set_peer_list(self, peer_list):
		self.__peer_list = peer_list

	def set_share_dir(self, share_dir):
		self.__share_dir = share_dir

	def flood_query(self, cmd):
		filename = cmd[1]
		try:
			for file in glob.glob(self.__share_dir):
				if file == filename:
					return 1
		except:
			return 0

	def tcp_server(self):
		tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# reuse port
		tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		tcp_server.bind(("127.0.0.1", self.__server_port))
		tcp_server.listen(5)
		print("start listening...")
		while True:
			conn, addr = tcp_server.accept()
			self.__source_ip_addr = conn
			print("addr: ", addr)
			while True:
				try:
					res = conn.recv(1024)
					# ['get', 'test.txt']
					self.__s_cmd = res.decode('utf-8').split()
					if self.__s_cmd[0] == 'get':
						
						self.__send(conn, self.__s_cmd[1])
					elif self.__s_cmd[0] == 'save':
						self.__save(conn)
				except ConnectionResetError:
					break
			conn.close()
			tcp_server.close()

	def __send(self, conn, filename):
		header_dic = {
			'filename': filename,
			'md5': 'xxdxx',
			'file_size': os.path.getsize(r'%s/%s' % (self.__share_dir, filename))
		}
		header_json = json.dumps(header_dic)
		header_bytes = header_json.encode('utf-8')

		# send header length
		conn.send(struct.pack('i', len(header_bytes)))

		# send header
		conn.send(header_bytes)

		# send data
		send_size = 0
		with open('%s/%s' % (self.__share_dir, filename), 'rb') as f:
			for b in f:
				conn.send(b)
				send_size += len(b)
				print(send_size)

	def __save(self, conn):
		obj = conn.recv(4)
		header_size = struct.unpack('i', obj)[0]

		# recv headers
		header_bytes = conn.recv(header_size)

		# unpack headers
		header_json = header_bytes.decode('utf-8')
		header_dic = json.loads(header_json)
		print(header_dic)
		total_size = header_dic['file_size']
		filename = header_dic['filename']

		# recv real data
		with open('%s/%s' % (self.__share_dir, filename), 'wb') as f:
			recv_size = 0
			while recv_size < total_size:
				res = conn.recv(1024)
				f.write(res)
				recv_size += len(res)
				print("total size: %s, already downloaded: %s" % (total_size, recv_size))

	def tcp_client(self):
		tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# need to be modified
		tcp_client.connect(('127.0.0.1', 802))
		print(tcp_client)
		print(111)
		while True:
			content = input(">>").strip()  # get test.txt
			if len(content) == 0:
				continue
			tcp_client.send(content.encode('utf-8'))
			self.__c_cmd = content.split()
			if self.__c_cmd[0] == 'get':
				self.__send(tcp_client, self.__c_cmd)
			elif self.__c_cmd[0] == 'save':
				self.__save(tcp_client)
		tcp_client.close()
