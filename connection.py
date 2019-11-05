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
import config


class Connection:
	# 自身属性
	__num = None
	__ip_addr = None
	__server_port = None
	__client_port = None
	__peer_list = None
	__share_dir = None
	__peer_num = 0

	# 当前对等方所有邻居的信息
	__peer_attr = []

	# 服务器端收到的命令
	__cmd = []

	__source_port = None
	__source_port = None

	def set_num(self, num):
		self.__num = int(num)

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

	def query(self, filename):
		try:
			for file in glob.glob(self.__share_dir):
				print(file)
				if file[file.find('\\')+1:] == filename:
					return 1
		except:
			return 0

		return 0

	def tcp_server(self):
		tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# 重用端口
		tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		tcp_server.bind(("127.0.0.1", self.__server_port))
		tcp_server.listen(5)
		print("start listening...")
		while True:
			conn, addr = tcp_server.accept()
			print("addr: ", addr)
			while True:
				try:
					res = conn.recv(1024)
					# ['get', 'test.txt']
					if not res:
						continue
					else:
						self.__cmd = res.decode('utf-8').split()
						if self.__cmd[0] == 'get':
							self.__source_port = self.__cmd[2]
							query_res = self.query(self.__cmd[1])
							print("%s: Query at self" % self.__num)
							if query_res == 0:
								print("%s: self failed, Querying neighbors" % self.__num)
								for i in self.__peer_attr:
									print("%s: querying neightbor %d" % (self.__num, int(i['server_port'])-800))
									self.tcp_client_query(i['ip_addr'], i['server_port'], res)
							else:
								msg = "found at %s" % self.__num
								self.tcp_client_notice("127.0.0.1", self.__source_port, msg)
								break
						elif self.__cmd[0] == 'found':
							print("success")
						else:
							msg = "invalid content"
							conn.send(msg.encode())
				except ConnectionResetError:
					break
				except:
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

	def tcp_client_query(self, ip, port, msg):
		tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tcp_client.connect((ip, int(port)))
		print(tcp_client)
		tcp_client.shutdown(2)
		tcp_client.close()

	def tcp_client_notice(self, ip, port, msg):
		tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tcp_client.connect((ip, int(port)))
		print(tcp_client)
		tcp_client.send(msg.encode())
		tcp_client.shutdown(2)
		tcp_client.close()

	def update_peer_attr(self):
		conf = config.Config()
		for i in self.__peer_list:
			self.__peer_attr = [conf.get_attr(i)]
			self.__peer_num += 1
		return self.__peer_attr
