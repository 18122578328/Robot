# -*- coding:utf-8 -*-
# -*- encoding: utf-8 -*-
# 测试环境: Python 3.6 版本

import socket
import sys
import numpy as np
import time
import math as m
# First import the library
import pyrealsense2 as rs


# Declare RealSense pipeline, encapsulating the actual device and sensors
pipe = rs.pipeline()

# Build config object and request pose data
cfg = rs.config()
cfg.enable_stream(rs.stream.pose)

# Start streaming with requested config
pipe.start(cfg)


# 直连模式下，机器人默认 IP 地址为 192.168.2.1, 控制命令端口号为 40923
host = "192.168.42.2"
port = 40923
# angle = 0

def main():
    t265_angle_array = {}  # t265两点连线与起步方向的夹角
    t265_distance_array = {}  # t265两点间距离
    # t265_angle1 = {}  # 临时变量，不用管
    t265_z_angle_array = {}  # t265转动角度的差值
    # 存放robo返回位置数据的数组
    new_x = {}
    new_y = {}
    new_z = {}
    robo_angle_array = {}  # robo两点连线与起步方向的夹角
    robo_distance_array = {}  # robo两点间距离
    robo_z_angle_array = {}  # robo转动角度的差值

    address = (host, int(port))

    # 与机器人控制命令端口建立 TCP 连接
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Connecting...")

    s.connect(address)

    print("Connected!")
    # 打开各个文件
    path = 'move_Robo_position_data.txt'
    f1 = open(path, 'w+')
    f1.write("三列数据分别表示Robo的x, y, z(Robo坐标系下向前走一米)")
    f1.write('\n')
    path = 'move_t265_position_data.txt'
    f2 = open(path, 'w+')
    f2.write("三列数据分别表示t265的x, y, z(t265坐标系下向前走一米)")
    f2.write('\n')
    path = 'move_t265_rotation_data.txt'
    f3 = open(path, 'w+')
    f3.write("三列数据分别表示t265的pitch, roll, yaw(t265坐标系下向前走一米)")
    f3.write('\n')
    # path = 'rotation_angle_data.txt'
    # f3 = open(path, 'w+')
    # 往返各记录一次，记录当前位置以用来对下一次位置的误差计算，所以i是跳2
    # for循环里第二位参数是控制实验次数
    try:
        # while True:
        for num in range(6):
            # Wait for the next set of frames from the camera
            frames = pipe.wait_for_frames()

            # Fetch pose frame
            pose = frames.get_pose_frame()
            if pose:
                # Print some of the pose data to the terminal
                data = pose.get_pose_data()
                # 等待用户输入控制指令
                msg = "command;"
                s.send(msg.encode('utf-8'))
                buf = s.recv(1024)
                msg = "chassis position ?;"
                # 发送控制命令给机器人
                s.send(msg.encode('utf-8'))
                buf = s.recv(1024)
                str1 = buf.decode('utf-8')
                print("Robo position: {}".format(str1))
                # 获得机械人返回的x,y,z
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
                new_y[num] = a[0, 0]
                new_x[num] = a[0, 1]
                new_z[num] = a[0, 2]
                Robo_position_x = str(new_x[num])
                f1.write('move前：')
                f1.write(Robo_position_x)
                f1.write(' \t ')
                Robo_position_y = str(new_y[num])
                f1.write(Robo_position_y)
                f1.write(' \t ')
                Robo_position_z = str(new_z[num])
                f1.write(Robo_position_z)
                f1.write(' \n ')
                front_data_position = data.translation
                t265_position_x = str(front_data_position.x)
                f2.write('move前：')
                f2.write(t265_position_x)
                f2.write(' \t ')
                t265_position_y = str(front_data_position.y)
                f2.write(t265_position_y)
                f2.write(' \t ')
                t265_position_z = str(front_data_position.z)
                f2.write(t265_position_z)
                f2.write(' \n ')
                w = data.rotation.w
                x = -data.rotation.z
                y = data.rotation.x
                z = -data.rotation.y
                pitch = -m.asin(2.0 * (x * z - w * y)) * 180.0 / m.pi
                roll = m.atan2(2.0 * (w * x + y * z), w * w - x * x - y * y + z * z) * 180.0 / m.pi
                yaw = m.atan2(2.0 * (w * z + x * y), w * w + x * x - y * y - z * z) * 180.0 / m.pi
                t265_pitch = str(pitch)
                f3.write('move前：')
                f3.write(t265_pitch)
                f3.write('\t')
                t265_roll = str(roll)
                f3.write(t265_roll)
                f3.write('\t')
                t265_yaw = str(yaw)
                f3.write(t265_yaw)
                f3.write('\n')
                # print("Frame #{}".format(pose.frame_number))
                # print("t265 Position: {}".format(data.translation))
                # 自行输入控制指令
                msg = "chassis move x 1;"
                s.send(msg.encode('utf-8'))
                buf = s.recv(1024)
                # 休眠8秒，即运行上一段代码的时间段为8秒
                time.sleep(12)
            # Wait for the next set of frames from the camera
            frames = pipe.wait_for_frames()

            # Fetch pose frame
            pose = frames.get_pose_frame()
            if pose:
                data = pose.get_pose_data()
                msg = "chassis position ?;"
                # 发送控制命令给机器人
                s.send(msg.encode('utf-8'))
                buf = s.recv(1024)
                str1 = buf.decode('utf-8')
                print("Robo position: {}".format(str1))
                # 获得机械人返回的x,y,z
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
                new_y[num + 1] = a[0, 0]
                new_x[num + 1] = a[0, 1]
                new_z[num + 1] = a[0, 2]
                Robo_position_x = str(new_x[num + 1])
                f1.write('move后：')
                f1.write(Robo_position_x)
                f1.write(' \t ')
                Robo_position_y = str(new_y[num + 1])
                f1.write(Robo_position_y)
                f1.write(' \t ')
                Robo_position_z = str(new_z[num + 1])
                f1.write(Robo_position_z)
                f1.write(' \n ')
                # print("t265 Position: {}".format(data.translation))
                late_data_position = data.translation
                t265_position_x = str(late_data_position.x)
                f2.write('move后：')
                f2.write(t265_position_x)
                f2.write(' \t ')
                t265_position_y = str(late_data_position.y)
                f2.write(t265_position_y)
                f2.write(' \t ')
                t265_position_z = str(late_data_position.z)
                f2.write(t265_position_z)
                f2.write(' \n ')
                w = data.rotation.w
                x = -data.rotation.z
                y = data.rotation.x
                z = -data.rotation.y
                # yaw_array[2 * num + 1] = m.atan2(2.0 * (w * z + x * y), w * w + x * x - y * y - z * z) * 180.0 / m.pi
                # yaw2 = m.atan2(2.0 * (w * z + x * y), w * w + x * x - y * y - z * z) * 180.0 / m.pi
                pitch = -m.asin(2.0 * (x * z - w * y)) * 180.0 / m.pi
                roll = m.atan2(2.0 * (w * x + y * z), w * w - x * x - y * y + z * z) * 180.0 / m.pi
                yaw = m.atan2(2.0 * (w * z + x * y), w * w + x * x - y * y - z * z) * 180.0 / m.pi
                t265_pitch = str(pitch)
                f3.write('move后：')
                f3.write(t265_pitch)
                f3.write('\t')
                t265_roll = str(roll)
                f3.write(t265_roll)
                f3.write('\t')
                t265_yaw = str(yaw)
                f3.write(t265_yaw)
                f3.write('\n')
            # handle data
            # 输出的是处理过的t265的数据
            # t265_distance_array[num] = pow(pow((late_data_position.x-front_data_position.x), 2) + pow(late_data_position.z-front_data_position.z, 2), 0.5)
            # robo_distance_array[num] = pow((pow((new_x[num+1]-new_x[num]), 2) + pow((new_y[num+1]-new_y[num]), 2)), 0.5)
            # distance = t265_distance_array[num] - robo_distance_array[num]
            # str_distance = str(distance)
            # f1.write(str_distance)
            # f1.write(' \t ')
            # t265_angle_array[num] = math.atan2(late_data_position.x - front_data_position.x, late_data_position.z - front_data_position.z)
            # robo_angle_array[num] = math.atan2(new_y[num+1]-new_y[num], new_x[num+1]-new_x[num])
            # angle = t265_distance_array[num] - robo_angle_array[num]
            # str_angle = str(angle)
            # f2.write(str_angle)
            # f2.write(' \t ')
            # t265_z_angle_array[num] = late_data_position.x - front_data_position.x
            # robo_z_angle_array[num] = new_z[num+1] - new_z[num]
            # rotation_angle = t265_z_angle_array[num] - robo_z_angle_array[num]
            # str_z_angle = str(rotation_angle)
            # f3.write(str_z_angle)
            # f3.write(' \t ')

    finally:
        pipe.stop()
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