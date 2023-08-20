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


def Pose():
    try:
        while True:
            # for num in range(num):
            # Wait for the next set of frames from the camera
            frames = pipe.wait_for_frames()

            # Fetch pose frame
            pose = frames.get_pose_frame()
            if pose:
                front_data_position = data.translation
                t265_position_x = front_data_position.x

                t265_position_y = front_data_position.y

                t265_position_z = front_data_position.z

                # Print some of the pose data to the terminal
                data = pose.get_pose_data()
                w = data.rotation.w
                x = -data.rotation.z
                y = data.rotation.x
                z = -data.rotation.y
                pitch = -m.asin(2.0 * (x * z - w * y)) * 180.0 / m.pi
                roll = m.atan2(2.0 * (w * x + y * z), w * w - x * x - y * y + z * z) * 180.0 / m.pi
                yaw = m.atan2(2.0 * (w * z + x * y), w * w + x * x - y * y - z * z) * 180.0 / m.pi
                print('{} {} {}'.format(t265_position_z, t265_position_x, yaw), end='\r')
    finally:
        pipe.stop()