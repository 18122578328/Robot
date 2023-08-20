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


def main():
    yaw_array = {}  # 自身角度
    new_z = {}  # 存放robo返回的z

    address = (host, int(port))

    # 与机器人控制命令端口建立 TCP 连接
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Connecting...")

    s.connect(address)

    print("Connected!")
    # 打开各个文件
    path = 'yaw_z_angle_data.txt'
    f1 = open(path, 'w+')
    try:
        for num in range(4):
            # Wait for the next set of frames from the camera
            frames = pipe.wait_for_frames()

            # Fetch pose frame
            pose = frames.get_pose_frame()
            if pose:
                # Print some of the pose data to the terminal
                data = pose.get_pose_data()
                w = data.rotation.w
                x = -data.rotation.z
                y = data.rotation.x
                z = -data.rotation.y
                yaw_array[2 * num] = m.atan2(2.0 * (w * z + x * y), w * w + x * x - y * y - z * z) * 180.0 / m.pi
                yaw1 = m.atan2(2.0 * (w * z + x * y), w * w + x * x - y * y - z * z) * 180.0 / m.pi
                print(yaw1)
                # 等待用户输入控制指令
                msg = "command;"
                s.send(msg.encode('utf-8'))
                buf = s.recv(1024)
                msg = "chassis position ?;"
                # 发送控制命令给机器人
                s.send(msg.encode('utf-8'))
                buf = s.recv(1024)
                str1 = buf.decode('utf-8')
                print(str1)
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
                # 多维数组的最后一个值赋予new_z
                new_z[num] = a[0, 2]
                # 自行输入控制指令
                msg = "chassis move z 360;"
                s.send(msg.encode('utf-8'))
                buf = s.recv(1024)
                # 休眠8秒，即运行上一段代码的时间段为8秒
                time.sleep(20)
            # Wait for the next set of frames from the camera
            frames = pipe.wait_for_frames()

            # Fetch pose frame
            pose = frames.get_pose_frame()
            if pose:
                data = pose.get_pose_data()
                w = data.rotation.w
                x = -data.rotation.z
                y = data.rotation.x
                z = -data.rotation.y
                yaw_array[2 * num + 1] = m.atan2(2.0 * (w * z + x * y), w * w + x * x - y * y - z * z) * 180.0 / m.pi
                yaw2 = m.atan2(2.0 * (w * z + x * y), w * w + x * x - y * y - z * z) * 180.0 / m.pi
                print(yaw2)
                msg = "chassis position ?;"
                # 发送控制命令给机器人
                s.send(msg.encode('utf-8'))
                buf = s.recv(1024)
                str1 = buf.decode('utf-8')
                print(str1)
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
                # 多维数组的最后一个值赋予new_z
                new_z[num + 1] = a[0, 2]
            yaw = yaw_array[2 * num + 1] - yaw_array[2 * num]
            robo_z = new_z[num + 1] - new_z[num]
            print(yaw)
            _ = robo_z - yaw
            yaw_z = str(_)
            f1.write(yaw_z)
            f1.write(' \t ')
    finally:
        pipe.stop()
    # 关闭所有文件
    f1.close()
    # 关闭端口连接
    time.sleep(5)
    s.shutdown(socket.SHUT_WR)
    s.close()


if __name__ == '__main__':
    main()
