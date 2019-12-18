# Query-flooding-based-Resource-Sharer
Keep Private until 2020
2019 年 11 月

**1.项目简介**

> 本项目基于洪泛(Flooding)技术实现了一个资源共享系统，可为用户提供**文件共享**、**共享资源下载**等服务。另外，该系统为用户提供了预置的**配置信息修改**服务。
>
> 为了更好地为测试者提供**直观的**测试界面以及**便捷的**测试方法，本项目提供了集成的可执行文件，通过模拟所在拓扑图的不同节点，测试者能够模拟不同对等方的真实操作。

**2.系统实现**

**2.1开发环境和工具**

> 操作系统： Windows 10 1903
>
> 处理器：Intel^®^ Core™ i7-8809G CPU @ 3.10GHz
>
> RAM: 16.0GB
>
> 开发工具： PyCharm 2019.2.3 (Professional Edition)
>
> 开发语言： Python 3.7.6

**2.2 系统设计**

> 本系统包含两个已封装的类：Config、Connection。

**2.2.1 Config**

**Config类**：

> get\_attr(i)：获取对等方"peer\_i"的信息，并打包以字典形式返回
>
> set\_attr(i)：对用户输入的数据检查后，修改对等方"peer\_i"的信息。
>
> modify(i, attr\_dict)：将对等方"peer\_i"的修改后信息写入配置文件。
>
> get\_ttl()：返回time to live值。
>
> get\_peer\_num()：获得当前网络环境中对等方的数量。
>
> \_\_init\_\_()：构造函数。

**2.2.2 Connection**

**Connection类**：

> set\_num(num)：设置节点编号。
>
> set\_ip(ip\_addr)：设置节点IP地址。
>
> set\_server\_port(server\_port)：设置节点的服务端端口。
>
> set\_client\_port(client\_port)：设置节点的客户端端口
>
> set\_peer\_list(peer\_list)：设置节点的邻居列表。
>
> set\_share\_dir(share\_dir)：设置资源共享本地目录。
>
> query(root, filename)：递归查询root目录下是否存在名为filename的文件。
>
> tcp\_handler(conn, addr)：tcp服务端在与客户端连接后的处理方法。
>
> tcp\_server()：tcp服务端基础建立。
>
> \_\_send(conn, filename)：在conn连接中发送名为filename的文件。
>
> \_\_save(conn)：保存从conn连接中收到的文件。
>
> tcp\_client\_notice(ip, port, msg)：节点调用自身的客户端口进行信息发送。
>
> update\_peer\_attr()：更新邻居属性字典。
>
> update\_ttl(msg)：更新消息中的time to live。

**2.2.3 其他函数**

**filemd5.py：**

> get\_file\_md5(file)：计算文件file的md5值。
>
> compare\_file\_md5(file, md5)：计算文件file的md5值并与传入的md5进行比较。

**process.py：**

> tcp\_server(ID)：用于多进程的tcp\_server函数。
>
> tcp\_client(role\_num, filename)：用于多进程的tcp\_client函数。

**3.关键技术点**

**3.1 配置文件读取/修改**

> 设计时采用**configparser**包，将其用于配置信息的**格式化文件读取**。在用户进行配置信息的修改时，系统将**对新信息的正确性予以确认**，并给予用户相应的**详细错误反馈**，方便用户进行修改更正。

**3.2 服务端支持并发**

> 本系统应用**多线程**，将TCP服务端对连接的处理方法封装，并在产生连接时**新建一个处理线程**，此时服务端继续监听其他并发连接。考虑到运行效率，在本项目中支持最高**5个并发**。

**3.3 文件传输检验**

> 本系统在进行文件传输前后，将对传输文件的正确性进行验证。
>
> 在本项目中，选用文件的**MD5值**为标准进行校验，通过在传输前后分别计算文件的MD5值，系统在接收完成后计算所接收文件的MD5值并与收到的MD5值进行比对，并反馈验证信息。

**3.4 多进程模拟服务端**

> 为了便于测试者的使用，本系统采用多进程的方式在主进程中用**进程池**的方法模拟各个对等方服务端的进程，并编写了简易的UI，方便测试者对系统反馈的各类信息进行阅读。

