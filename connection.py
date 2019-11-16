#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = "connection.py"
__author__ = "louis"
__mtime__ = "2019/11/5"
"""
import socket
import threading
import os
import struct
import json
import config
import zipfile
import filemd5


class Connection:
	# 自身属性
	__num = None
	__ip_addr = None
	__server_port = None
	__client_port = None
	__peer_list = None
	__share_dir = None
	__peer_num = 0
	__query_res = dict()
	__path_list = dict()
	__timeout_flag = dict()

	# 当前对等方所有邻居的信息
	__peer_attr = []

	# 服务器端收到的命令
	__cmd = []

	__source_ip = '127.0.0.1'
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

	def query(self, root, filename):
		items = os.listdir(root)
		for item in items:
			path = os.path.join(root, item)
			print(path.split("/"))
			if path.split('\\')[-1] == filename or path.split('/')[-1] == filename:
				self.__query_res[filename] = 1
				self.__path_list[filename] = path.replace('\\', '/')
			elif os.path.isdir(path):
				self.query(path.replace('\\', '/'), filename)

	def tcp_handler(self, conn, addr):
		print("addr: ", addr)
		while True:
			try:
				res = conn.recv(1024)

				# [[ordertype], [filename], [port], [ip], [ttl]]

				if not res:
					continue
				else:
					print(res.decode())
					self.__cmd = res.decode('utf-8').split()

					if self.__cmd[0] == 'get':
						res = self.update_ttl(res)
						self.__source_port = self.__cmd[2]
						self.__source_ip = self.__cmd[3]
						self.__query_res[self.__cmd[1]] = 0
						self.query(self.__share_dir, self.__cmd[1])
						print("%s: Query %s at self" % (self.__num, self.__cmd[1]))

						# 本地未找到，查询邻居节点
						if self.__query_res[self.__cmd[1]] == 0:
							if int(self.__cmd[-1]) >= 0:
								print("%s: self failed, Querying neighbors" % self.__num)
								for i in self.__peer_attr:
									print("%s: querying neighbor %d" % (self.__num, int(i['server_port']) - 800))
									self.tcp_client_notice(i['ip_addr'], i['server_port'], res)

							else:
								print("over ttl")

						# 本地找到，向请求源server发送成功消息
						else:
							msg = "found %s at %s %s %s" % (
								self.__cmd[1], self.__num, self.__ip_addr, self.__server_port)
							self.tcp_client_notice(self.__source_ip, self.__source_port, msg)

					# 收到“found filename at x [ip] [port]”消息，即向x的server发送请求
					elif self.__cmd[0] == 'found':
						self.__timeout_flag[self.__cmd[1]] = 0
						self.__source_ip = self.__cmd[4]
						self.__source_port = self.__cmd[5]
						msg = 'request %s %s %s' % (self.__cmd[1], self.__ip_addr, self.__server_port)
						self.tcp_client_notice(self.__source_ip, self.__source_port, msg)

					# 收到“request filename [ip] [port]”消息，即向请求源发送文件
					elif self.__cmd[0] == 'request':
						self.__send(conn, self.__cmd[1])

					# 过滤其它命令
					else:
						msg = "invalid content"
						conn.send(msg.encode())

					break
			except ConnectionResetError:
				break
		conn.close()

	def tcp_server(self):
		tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		tcp_server.bind(("127.0.0.1", self.__server_port))
		tcp_server.listen(5)
		while True:
			try:
				conn, addr = tcp_server.accept()
			except ConnectionAbortedError:
				continue
			t = threading.Thread(target=self.tcp_handler, args=(conn, addr))
			t.start()

	def __send(self, conn, filename):
		true_name = filename
		filepath = self.__path_list[filename]
		if filename.find('.') != -1:
			filename = filename[0:filename.find('.')] + ".zip"
		else:
			filename = filename + ".zip"
		z = zipfile.ZipFile(filename, 'w')
		if os.path.isdir(filepath):
			for d in os.listdir(filepath):
				z.write(filepath + os.sep + d, d)
		else:
			z.write(filepath, true_name)
		z.close()

		header_dic = {
			'filename': filename,
			'md5': filemd5.get_file_md5(filename),
			'file_size': z.infolist()[0].file_size
		}
		header_json = json.dumps(header_dic)
		header_bytes = header_json.encode('utf-8')

		# 打包文件头
		conn.send(struct.pack('i', len(header_bytes)))

		# 发送头
		conn.send(header_bytes)

		# 发送数据
		send_size = 0
		with open(filename, 'rb') as f:
			for b in f:
				conn.send(b)
				send_size += len(b)
				print(send_size)

		os.remove(filename)

	def __save(self, conn):
		obj = conn.recv(4)
		header_size = struct.unpack('i', obj)[0]

		# 接收头
		header_bytes = conn.recv(header_size)

		# 解包头
		header_json = header_bytes.decode('utf-8')
		header_dic = json.loads(header_json)
		print(header_dic)
		total_size = header_dic['file_size']
		filename = header_dic['filename']
		cur_md5 = header_dic['md5']

		# 接收数据
		with open('%s%s' % (self.__share_dir, filename), 'wb') as f:
			recv_size = 0
			while recv_size < total_size:
				res = conn.recv(1024)
				f.write(res)
				recv_size += len(res)
			print("total size: %s, already downloaded: %s" % (total_size, recv_size))
		if filemd5.compare_file_md5('%s%s' % (self.__share_dir, filename), cur_md5) == 1:
			z = zipfile.ZipFile("%s%s" % (self.__share_dir, filename), 'r')
			print(z)
			z.extractall("%s" % self.__share_dir)
			z.close()
		else:
			print("file corrupt during transmission")
		os.remove("%s%s" % (self.__share_dir, filename))

	def tcp_client_notice(self, ip, port, msg):
		tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tcp_client.connect((ip, int(port)))
		print(tcp_client)
		tcp_client.send(msg.encode())
		if msg.split()[0] == 'request':
			self.__save(tcp_client)
		if msg.split()[0] == 'get':
			self.__timeout_flag[msg.split()[1]] = 1
		tcp_client.shutdown(2)
		tcp_client.close()

	def update_peer_attr(self):
		conf = config.Config()
		for i in self.__peer_list:
			if not i:
				break
			else:
				self.__peer_attr = [conf.get_attr(i)]
				self.__peer_num += 1
		return self.__peer_attr

	def update_ttl(self, msg):
		msg = msg.decode().split()
		msg[-1] = str(int(msg[-1]) - 1)
		new_msg = " ".join(msg)
		return new_msg

	def get_timeout_flag(self):
		return self.__timeout_flag
