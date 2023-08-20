# -*- coding:utf-8 -*-
# -*- encoding: utf-8 -*-
# 测试环境: Python 3.6 版本

import socket
import sys
import numpy as np
from rm_sdk import s

# 直连模式下，机器人默认 IP 地址为 192.168.2.1, 控制命令端口号为 40923
host = "192.168.2.1"
port = 40923


def return_position():
    global a
    # 等待用户输入控制指令
    msg = "chassis position ?;"
    # 发送控制命令给机器人
    s.send(msg.encode('utf-8'))
    buf = s.recv(1024)
    str = buf.decode('utf-8')

    print(str)

    count = 0
    counta = 0
    a = np.zeros((1, 3))  # 创建一个多维数组[[0. 0. 0.]]
    temp0 = 0
    for n in str:
        count += 1
        if n == ' ':
            a[0, counta] = float(str[temp0:count])
            counta += 1
            temp0 = count - 1


def multiTrail():
    address = (host, int(port))

    # 与机器人控制命令端口建立 TCP 连接
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Connecting...")

    s.connect(address)

    print("Connected!")
    error = [(0, 0) for i in range(100)]  # 误差数组
    now_position = [(0, 0) for i in range(100)]  # 当前位置
    distance = [(0, 0) for i in range(100)]  # 两点距离
    new_x = 0
    new_y = 0
    m_array = []
    a_array = []
    while True:
        for i in range(0, 100, 2):
            # 来回各记录一次，记录当前位置以用来对下一次位置的误差计算，所以i是跳2
            s.command("chassis move x 1 y 1 wait_for_complete false")
            return_position()
            new_x = a[0, 0]
            new_y = a[0, 1]
            # new_x, new_y记为返回的position
            # if i > 0:
            #     fir_m[i-1] = pow(new_x, 2) + pow(new_y, 2)
            if i > 1:
                now_position[i] = (new_x, new_y)
                a_array.append(np.arctan(
                    [(now_position[i][0] - now_position[i - 1][0]), (now_position[i][1] - now_position[i - 1][1])]))
                path = 'a_data.txt'
                f = open(path, 'w+')
                f.write(a_array[i])
                f.close()
                distance[i] = now_position[i] - now_position[i - 1]
                m_array.append(pow((pow(distance[i][0], 2) + pow(distance[i][1], 2)), 0.5) - pow(2, 0.5))
                path = 'm_data.txt'
                f = open(path, 'w+')
                f.write(m_array[i])
                f.close()
                error[i] = distance[i] - (1, 1)
                path = 'error.txt'
                f = open(path, 'w+')
                f.write(error[i])
                f.close()
            else:
                distance[i] = now_position[i] = (new_x, new_y)
                a_array.append(np.arctan([now_position[i][0], now_position[i][1]]))
                path = 'a_data.txt'
                f = open(path, 'w+')
                f.write(a_array[i])
                f.close()
                m_array.append(pow((pow(distance[i][0], 2) + pow(distance[i][1], 2)), 0.5) - pow(2, 0.5))
                path = 'm_data.txt'
                f = open(path, 'w+')
                f.write(m_array[i])
                f.close()
                error[i] = distance[i] - (1, 1)
                path = 'error.txt'
                f = open(path, 'w+')
                f.write(error[i])
                f.close()
            s.command("chassis move x -1 y -1 wait_for_complete false")
            return_position()
            new_x = a[0, 0]
            new_y = a[0, 1]
            # new_x, new_y记为返回的position
            if i < 99:
                now_position[i + 1] = (new_x, new_y)
                a_array.append(np.arctan(
                    [(now_position[i][0] - now_position[i + 1][0]), (now_position[i][1] - now_position[i + 1][1])]))
                path = 'a_data.txt'
                f = open(path, 'w+')
                f.write(a_array[i])
                f.close()
                distance[i + 1] = now_position[i] - now_position[i + 1]
                m_array.append(pow((pow(distance[i][0], 2) + pow(distance[i][1], 2)), 0.5) - pow(2, 0.5))
                path = 'm_data.txt'
                f = open(path, 'w+')
                f.write(m_array[i])
                f.close()
                error[i + 1] = distance[i + 1] - (1, 1)
                path = 'error.txt'
                f = open(path, 'w+')
                f.write(error[i])
                f.close()
        # 关闭端口连接
        s.shutdown(socket.SHUT_WR)
        s.close()


if __name__ == '__main__':
    multiTrail()
