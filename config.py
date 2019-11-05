#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ""
__author__ = "louis"
__mtime__ = "2019/11/5"
"""
import configparser
import ipaddress


class Config:
    __cf = configparser.ConfigParser()
    __ttl = 0

    def get_attr(self, i):
        """
        :param i: represent the sequence number of peer e.g. [peer-i]
        :return: dict {'ip_addr': ip, 'port': port, 'share_dir': share_dir, 'peer_list': peer_list}
        """
        peer = dict()
        peer['ip_addr'] = self.__cf.get("Peer-%s" % i, "ip_addr")
        peer['server_port'] = self.__cf.get("Peer-%s" % i, "server_port")
        peer['client_port'] = self.__cf.get("Peer-%s" % i, "client_port")
        peer['share_dir'] = self.__cf.get("Peer-%s" % i, "share_dir")
        peer_str = self.__cf.get("Peer-%s" % i, "peer_list")
        peer_str = peer_str[1:len(peer_str) - 1]
        peer_list = peer_str.split(', ')
        for i in range(len(peer_list)):
            peer_list[i] = int(peer_list[i])
        peer['peer_list'] = peer_list
        return peer

    def set_attr(self, i, attr_dict):
        """
        :param i: represent the sequence number of peer e.g. [peer-i]
        :param attr_dict: the dict of new attributes
        :return: modify info
        """
        self.__init__()
        origin_attr = self.get_attr(i)
        diff_val = [(k, origin_attr[k], attr_dict[k]) for k in origin_attr if origin_attr[k] != attr_dict[k]]
        # e.g.[('diff_key', original_attr[diff_key], attr_dict[diff_key])]
        if not diff_val:
            return "No modification found"
        for t in diff_val:
            ori = []
            for j in range(self.get_peer_num()):
                sin = self.get_attr(j)
                ori.append(sin[t[0]])

            if t[2] in ori:
                return "Duplicate %s" % t[0]

            if t[0] == 'ip_addr':
                if not ipaddress.ip_address(t[2]):
                    return "Invalid ip_addr"

        self.__modify(i, attr_dict)
        return "Modify success"

    def __modify(self, i, attr_dict):
        data = ""
        flag = 0
        attr_dict["peer_list"] = str(attr_dict["peer_list"])
        with open("config.ini", "r") as f:
            for line in f:
                if flag > 0:
                    flag -= 1

                if "Peer-%s" % i in line:
                    flag = 6

                if flag == 5:
                    line = line.replace(line[line.find("=") + 2:len(line) - 1], attr_dict["ip_addr"])
                elif flag == 4:
                    line = line.replace(line[line.find("=") + 2:len(line) - 1], attr_dict["server_port"])
                elif flag == 3:
                    line = line.replace(line[line.find("=") + 2:len(line) - 1], attr_dict["client_port"])
                elif flag == 2:
                    line = line.replace(line[line.find("=") + 2:len(line) - 1], attr_dict["share_dir"])
                elif flag == 1:
                    line = line.replace(line[line.find("=") + 2:len(line) - 1], attr_dict["peer_list"])

                data += line
        with open("config.ini", "w") as f:
            f.write(data)

    def get_ttl(self):
        return self.__ttl

    def set_ttl(self, ttl):
        self.__ttl = ttl

    @staticmethod
    def get_peer_num():
        with open("config.ini", "r") as f:
            count = 0
            for line in f:
                count += 1
        return int((count + 1) / 7)

    def __init__(self):
        self.__cf.read("config.ini")
        self.__ttl = 2

