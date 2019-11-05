#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ""
__author__ = "louis"
__mtime__ = "2019/11/5"
"""
import config
import connection


init_config = config.Config()
peer_1 = init_config.get_attr(1)
peer_c = connection.Connection()
peer_c.set_ip(peer_1['ip_addr'])
peer_c.set_server_port(peer_1['server_port'])
peer_c.set_client_port(peer_1['client_port'])
peer_c.set_share_dir(peer_1['share_dir'])
peer_c.set_peer_list(peer_1['peer_list'])
peer_c.tcp_client()