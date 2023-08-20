# -*- coding:utf-8 -*-
# -*- encoding: utf-8 -*-
# 测试环境: Python 3.6 版本

import socket
import sys
import numpy as np
import time
import math
from expe import *

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

    while True:
        # 等待用户输入控制指令
        msg = "command;"
        s.send(msg.encode('utf-8'))
        buf = s.recv(1024)
        # 自行输入控制指令
        msg = input("输入旋转角度：")  # 看看能不能和嘉强的输入函数结合
        # 当用户输入 Q 或 q 时，退出当前程序
        if msg.upper() == 'Q':
            break
        msg += ';'
        s.send(msg.encode('utf-8'))
        buf = s.recv(1024)
        # 休眠8秒，即运行上一段代码的时间段为8秒
        time.sleep(8)
        msg = input("输入移动距离：")

        # 当用户输入 Q 或 q 时，退出当前程序
        if msg.upper() == 'Q':
            break

        # 添加结束符
        msg += ';'

        # 发送控制命令给机器人
        s.send(msg.encode('utf-8'))
        buf = s.recv(1024)
        # 等待用户输入控制指令
        time.sleep(5)
        expe.observe()
        time.sleep(60)

        s.send(msg.encode('utf-8'))
        buf = s.recv(1024)
        time.sleep(8)
        msg = "chassis position ?;"
        # 发送控制命令给机器人
        s.send(msg.encode('utf-8'))
        buf = s.recv(1024)
        str1 = buf.decode('utf-8')

        print(str1)
        # 获取机械人的x,y,z
        count = 0
        counta = 0
        a = np.zeros((1, 3))  # 创建一个多维数组[[0. 0. 0.]]
        temp0 = 0
        for n in str1:
            count += 1
            if n == ' ':
                a[0, counta] = float(str1[temp0:count])
                counta += 1
                temp0 = count - 1
        # 多维数组的三个值分别赋予new_x,new_y,new_z
        new_x1 = a[0, 0]
        new_y1 = a[0, 1]
        new_z1 = a[0, 2]
        now_position1
        time.sleep(5)
        msg = "chassis move x 1"

        # 当用户输入 Q 或 q 时，退出当前程序
        if msg.upper() == 'Q':
            break

        # 添加结束符
        msg += ';'

        # 发送控制命令给机器人
        s.send(msg.encode('utf-8'))
        buf = s.recv(1024)
        # 等待用户输入控制指令
        time.sleep(5)
        msg = "chassis position ?;"
        # 发送控制命令给机器人
        s.send(msg.encode('utf-8'))
        buf = s.recv(1024)
        str1 = buf.decode('utf-8')

        print(str1)
        # 获取机械人的x,y,z
        count = 0
        counta = 0
        a = np.zeros((1, 3))  # 创建一个多维数组[[0. 0. 0.]]
        temp0 = 0
        for n in str1:
            count += 1
            if n == ' ':
                a[0, counta] = float(str1[temp0:count])
                counta += 1
                temp0 = count - 1
        # 多维数组的三个值分别赋予new_x,new_y,new_z
        new_x = a[0, 0]
        new_y = a[0, 1]
        new_z = a[0, 2]
        # new_x, new_y记为返回的position
        # 这一段if...是返，即从某一地点返回
        if i < 99:
            # 当前位置
            now_position[i + 1] = (new_x, new_y, new_z)
            # 自身角度的差值
            a_array.append(now_position[i+1][2] - now_position[i][2])
            # 写进"a_data.txt"
            strA = str(a_array[i])
            f1.write(strA)
            f1.write(' \t ')
            # 两点间x, y的差值
            distance[i + 1] = (now_position[i][0] - now_position[i + 1][0], now_position[i][1] - now_position[i + 1][1])
            # 两点间距离的误差
            m_array.append(pow((pow(distance[i][0], 2) + pow(distance[i][1], 2)), 0.5) - 1)
            # 写进"m_data.txt"
            strM = str(m_array[i])
            f2.write(strM)
            f2.write(' \t ')
            # x的误差
            errorX[i+1] = abs(distance[i+1][0] - 1)
            # 写进"error.txt"中的第一列
            strErrX = str(errorX[i])
            f3.write(strErrX)
            f3.write(' \t ')
            # y的误差
            errorY[i+1] = abs(distance[i+1][1] - 0)
            # 写进"error.txt"中的第二列
            strErrY = str(errorY[i])
            f3.write(strErrY)
            f3.write(' \n ')
        time.sleep()
    # 关闭所有文件
    f1.close()
    f2.close()
    f3.close()
    # 关闭端口连接
    time.sleep(5)
    s.shutdown(socket.SHUT_WR)
    s.close()


if __name__ == '__main__':
    main()
