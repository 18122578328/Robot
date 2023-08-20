#!/usr/bin/env python3
# coding=utf-8

# import sys
import time
# import threading
import socket
import EKF
import numpy as np
import math
import visualization as vis
from expe import *

IP_LIST = ['192.168.45.248', '192.168.45.55' ] #robomaster的IP列表'192.168.200.248',
EP_DICT = {}
n = len(IP_LIST) #机器人个数
z = np.zeros((n, 1)) #旋转命令集
D = np.zeros((n, 1)) #直走命令集
pos_start = np.zeros((3*n, 1)) #起始世界坐标
pos_now = np.zeros((3*n, 1)) #当前时刻机器坐标
now_POSITION = np.zeros((3 * n, 1)) #当前时刻世界坐标

Q_xz = np.diag([1, 2, 3, 4, 5, 6]) #状态矩阵的旋转方差
Q_zz = np.diag([6, 5, 4, 3, 2, 1]) #状态矩阵的直走方差
R_k = np.diag([2, 4, 6, 8]) #观测矩阵的方差
final_Xk_zz = np.zeros((3*n, 1))

class EP:
    def __init__(self, ip):
        self.IP = ip
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #套接字连接

    def exit(self):  #断连函数
        self.s.shutdown(socket.SHUT_WR)
        self.s.close()

    def start(self): #进入robomaster命令模式
        global address
        address = (self.IP, 40923)
        self.s.connect(address)
        msg0 = "command;"
        self.s.send(msg0.encode('utf-8'))
        buf = self.s.recv(1024)
        print(buf)

    def inStart_pos(self, k): #输入开始时机器人的世界坐标，存到pos_start中
        x1 = input("Please enter the start world position x \n")
        y1 = input("Please enter the start world position y \n")
        z1 = input("Please enter the start world position z \n")
        pos_start[k, 0] = float(x1)
        pos_start[k+1, 0] = float(y1)
        pos_start[k+2, 0] = float(z1)

    def get_start_position(self): #获取运动前机器人的机器坐标
        global pos0
        # msg = "chassis position ?;"
        # self.s.send(msg.encode('utf-8'))
        # buf = self.s.recv(1024)
        # temp = buf.decode('utf-8')
        # temp = temp.split()
        # x, y, z = float(temp[0]), float(temp[1]), float(temp[2])
        observe()
        pos0 = observe_handle()
        print(pos0)

    def get_real_start_position(self, k, i): #获取运动前机器人的世界坐标并存放至
        if i != 0:
            pos_start[k, 0] = final_Xk_zz[k, 0]
            pos_start[k + 1, 0] = final_Xk_zz[k + 1, 0]
            pos_start[k + 2, 0] = final_Xk_zz[k + 2, 0]

    def move_command_z(self, i): #输入旋转命令
        global pos1
        z1 = input('please enter z')
        self.s.sendto(f"chassis move x 0 y 0 z {z1};".encode('utf-8'), address)
        buf = self.s.recv(1024)
        z1 = float(z1)
        z[i, 0] = z1
        temp = (0, 0, z1)
        print('%s:move %s' % (self.IP, temp))
        zipped = zip(pos0, temp)
        mapped = map(sum, zipped)
        pos1 = tuple(mapped) #旋转后的理论位置
        print('%s:%s' % (self.IP, pos1))
        time.sleep(4)

    def move_command_x(self, j): #输入直走命令
        global pos2
        x1 = input('please enter x')
        self.s.sendto(f"chassis move x {x1} y 0 z 0;".encode('utf-8'), address)
        buf = self.s.recv(1024)
        x1 = float(x1)
        D[j, 0] = x1
        temp2 = (x1, 0, 0)
        temp1 = x1 * math.cos((pos1[2] - pos0[2]) * math.pi / 180)
        temp6 = x1 * math.sin((pos1[2] - pos0[2]) * math.pi / 180)
        temp = (temp1, temp6, 0)
        print('%s:move %s' % (self.IP, temp2))
        zipped = zip(pos1, temp)
        mapped = map(sum, zipped)
        pos2 = tuple(mapped) #直走后的理论位置
        print('%s:%s' % (self.IP, pos2))
        time.sleep(4)

    def get_now_position(self, k):  # 现在坐标
        global pos3, world_pos
        # msg = "chassis position ?;"
        # self.s.send(msg.encode('utf-8'))
        # buf = self.s.recv(1024)
        # temp = buf.decode('utf-8')
        # temp = temp.split()
        # x1, y1, z1 = float(temp[0]), float(temp[1]), float(temp[2])
        observe()
        pos3 = observe_handle() #机器坐标
        pos_now[k, 0] = pos3[0]
        pos_now[k+1, 0] = pos3[1]
        pos_now[k+2, 0] = pos3[2]
        x2, y2, z2 = pos0[0], pos0[1], pos0[2]

        now_POSITION[k, 0] = pos_start[k, 0] + (x1 - x2) * math.cos(
            pos_start[k+2, 0] * math.pi / 180) - (y1 - y2) * math.sin(
            pos_start[k+2, 0] * math.pi / 180)
        now_POSITION[k + 1, 0] = pos_start[k+1, 0] + (x1 - x2) * math.sin(
            pos_start[k+2, 0] * math.pi / 180) + (y1 - y2) * math.cos(
            pos_start[k+2, 0] * math.pi / 180)
        now_POSITION[k + 2, 0] = pos_start[k+2, 0] + (z1 - z2)        #计算得到的世界坐标
        world_pos = (now_POSITION[k, 0], now_POSITION[k+1, 0], now_POSITION[k+2, 0])
        print('%s:%s' % (self.IP, pos3))
        print('%s:%s' % (self.IP, world_pos))


# def EKF_position(P_old_xz, Q_xz, R_k, X_old_xz, z, P_old_zz, Q_zz, X_old_zz, D):
def EKF_position(P_old_xz, pos_start, z, P_old_zz, D):
    f_xz, P_k_xz = EKF.final_xz(now_POSITION, P_old_xz, Q_xz, R_k, pos_start, z)
    time.sleep(5)
    f_zz, P_k_zz = EKF.final_zz(R_k, now_POSITION, P_old_zz, Q_zz, pos_start, D, f_xz)
    return f_zz


if __name__ == "__main__":
    a = 0
    for ip in IP_LIST:
        print('%s connecting...' % ip)
        EP_DICT[ip] = EP(ip)
        EP_DICT[ip].start()
        EP_DICT[ip].inStart_pos(a)
        a = a + 3
    P_old_xz = np.ones((3 * n, 3 * n))  #旋转的预测误差阵
    P_old_zz = np.ones((3 * n, 3 * n))  #直走的预测误差阵

    b = 0
    while True:
        k = 0
        i = 0
        for ip in IP_LIST:
            EP_DICT[ip].get_start_position()
            time.sleep(10)

            EP_DICT[ip].get_real_start_position(k, b)

            EP_DICT[ip].move_command_z(i)

            time.sleep(4)

            EP_DICT[ip].move_command_x(i)
            i = i + 1

            time.sleep(10)

            EP_DICT[ip].get_now_position(k)
            k = k + 3
        b = b + 1
        # P_old_xz,Q_xz,R_k,X_old_xz,z，P_old_zz, Q_zz, X_old_zz, D为手动输入的数值
        final_Xk_zz = EKF_position(P_old_xz, pos_start, z, P_old_zz, D)
        print(final_Xk_zz)
        vis.show(final_Xk_zz,IP_LIST)
    # for ip in IP_LIST:
    #     EP_DICT[ip].exit()