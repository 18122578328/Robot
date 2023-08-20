# -*- coding:utf-8 -*-
# -*- encoding: utf-8 -*-
# 测试环境: Python 3.6 版本

import socket
import sys
import time

# 直连模式下，机器人默认 IP 地址为 192.168.2.1, 控制命令端口号为 40923
host = "192.168.2.1"
port = 40923


def main():
    address = (host, int(port))

    # 与机器人控制命令端口建立 TCP 连接
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Connecting...")

    s.connect(address)

    print("Connected!")

    # 等待用户输入控制指令
    msg = "command;"
    s.send(msg.encode('utf-8'))
    buf = s.recv(1024)
    time.sleep(2)
    msg = "chassis position ?;"
    # 发送控制命令给机器人
    s.send(msg.encode('utf-8'))
    buf = s.recv(1024)
    str1 = buf.decode('utf-8')
    print(str1)
    msg = "chassis moveto x 0 y 0"

    # 当用户输入 Q 或 q 时，退出当前程序

    # 添加结束符
    msg += ';'

    # 发送控制命令给机器人
    s.send(msg.encode('utf-8'))

    try:
        # 等待机器人返回执行结果
        buf = s.recv(1024)

        print(buf.decode('utf-8'))
        time.sleep(5)
        msg = "chassis position ?;"
        # 发送控制命令给机器人
        s.send(msg.encode('utf-8'))
        buf = s.recv(1024)
        str1 = buf.decode('utf-8')
        print(str1)
    except socket.error as e:
        print("Error receiving :", e)
        sys.exit(1)


    # 关闭端口连接
    time.sleep(10)
    s.shutdown(socket.SHUT_WR)
    s.close()

if __name__ == '__main__':
    main()
