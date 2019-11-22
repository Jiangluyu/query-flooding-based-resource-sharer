# config.ini
包含内容：
    各个对等方的预设值
        ip地址
        端口号
        共享目录
        对等方列表
    ttl
格式示例：

[Peer-1]
ip_addr = 127.0.0.1 # 修改成预设的ip地址
port = 81 # 修改成预设的端口号
share_dir = "/Users/louis/PycharmProjects/nwclass/1/"
peer_list = [3, 4, 5]

[Peer-0]
ip_addr = 127.0.0.1
port = 80
share_dir = "/Users/louis/PycharmProjects/nwclass/My/"
peer_list = [1, 2]

[settings]
ttl = 2

预设的config中，连接方式如下：
           ___0___
          |          |
       __1__      2__
       |   |   |         |
      3  4  5         6
