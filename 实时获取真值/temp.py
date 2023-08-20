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
# another code
import apriltag
import cv2
import os

# another code

# Points3DAll = np.array([[[ 0, 74, 0],[74, 74, 0],[74, 0, 0],[0, 0, 0]]], dtype = "double")
Points3DAll = np.array([[[-168.75, 154.13, 75], [-168.75, 80.13, 75], [-168.75, 80.13, 1], [-168.75, 154.13, 1]],
                       [[-84.75,159.13,75],[-158.75,159.13,75],[-158.75,159.13,1],[-84.75,159.13,1]],
                       [[166.75,162.5,75],[92.75,162.5,75],[92.75,162.5,1],[166.75,162.5,1]],
                       [[184.75,83.5,75],[184.5,157.5,75],[184.75,157.5,1],[184.75,83.5,1]],
                       [[158.75,-154.13,75],[158.75,-80.13,75],[158.75,-80.13,1],[158.75,-154.13,1]],
                       [[79.75,-159.13,75],[153.75,-159.13,75],[153.75,-159.13,1],[79.75,-159.13,1]],
                       [[-153.75,-159.13,75],[-79.75,-159.13,75],[-79.75,-159.13,1],[-153.75,-159.13,1]],
                       [[-158.75,-80.13,75],[-158.75,-154.13,75],[-158.75,-154.13,1],[-158.75,-80.13,1]],
                       [[0, 0, 0], [0, 180, 0], [180, 180, 0], [0, 180, 0]]], dtype="double")     # Last Column for landmark
# print(Points3DAll.shape)

Points3DAllIndex = np.array([[4]])
MaxIndex = 15

Wid = 1920
Hei = 1080

pipe = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, Wid, Hei, rs.format.bgr8, 30)
cfg = pipe.start(config)
for i in range(40):
    pipe.wait_for_frames()
frame = pipe.wait_for_frames()
Color = frame.get_color_frame()
CProfile = cfg.get_stream(rs.stream.color)
CIntrin = CProfile.as_video_stream_profile().get_intrinsics()
CamIn = np.array([[CIntrin.fx, 0.0, CIntrin.ppx], [0.0, CIntrin.fy, CIntrin.ppy], [0.0, 0.0, 1.0]])
CDistortCoe = np.array(CIntrin.coeffs)

# Declare RealSense pipeline, encapsulating the actual device and sensors
pipe1 = rs.pipeline()

# Build config object and request pose data
cfg1 = rs.config()
cfg1.enable_stream(rs.stream.pose)

# Start streaming with requested config
pipe1.start(cfg1)


# another code
def PnPProcess(Points3D, Points0, CamIn, CDistortCoe):
    retval, RVec, TVec = cv2.solvePnP(Points3D, Points0, CamIn, CDistortCoe,
                                      flags=cv2.SOLVEPNP_ITERATIVE)  # useExtrinsicGuess = False,cv2.SOLVEPNP_EPNP
    RotWCam, Jacobian = cv2.Rodrigues(RVec)
    temp_rot=np.array([[1,0,0],[0,0,1],[0,-1,0]],dtype="double")
    RotWCam = np.matmul(temp_rot, RotWCam)
    TVec=np.matmul(temp_rot,TVec) + np.array([[-154.5],[156.18],[87.5]])
    RotCamW = RotWCam.T
    CamW = np.dot(-RotCamW, TVec)
    #return (str(CamW[0, 0]).ljust(20), str(CamW[1, 0]).ljust(20), str(CamW[2, 0]).ljust(20),
    #        str(RVec[0, 0]).ljust(20), str(RVec[1, 0]).ljust(20), str(RVec[2, 0]).ljust(20))
    # return [(CamW[0]**2 + CamW[1]**2)**(1/2), m.atan2(CamW[1], CamW[0]), np.linalg.norm(RVec)]
    return [CamW[0, 0], CamW[1, 0], np.linalg.norm(RVec)]

def Pose():
    try:
        while True:
            # another code
            frame = pipe.wait_for_frames()
            Color = frame.get_color_frame()
            Color_np = np.asanyarray(Color.get_data())

            Gray_np = cv2.cvtColor(Color_np, cv2.COLOR_BGR2GRAY)
            # print("Ready")
            Options = apriltag.DetectorOptions(quad_decimate=2.0)
            detections = apriltag.Detector(options=Options)
            # detections = apriltag.Detector(families='tag36h11', quad_decimate=2)
            tags = detections.detect(Gray_np)
            # print("Detected")
            pnp_result = [0, 0, 0]
            see = False
            if len(tags) != 0:
                count = 0
                for tag in tags:
                    ID = tag.tag_id
                    count = count + 1
                    # print(ID)
                    if ID == 16:
                        Point2DNp = np.array(tag.corners)
                        Point3D = Points3DAll[8, 0:4, 0:3]
                        LandMark_result = PnPProcess(Point3D, Point2DNp, CamIn, CDistortCoe)
                        see = True
                        break
                    elif ID <= MaxIndex:
                        master_numb = ID//8
                        Point2DNp = np.array(tag.corners)  ###########
                        # print(Point2DNp)Point3D = Points3DAll[int(ID), 0:4, 0:3]
                        Point3D = Points3DAll[int(ID%8), 0:4, 0:3]

                        # Point3D = Points3DAll[0, 0:4, 0:3]
                        # print(Point3D.shape)
                        # Point2D = Points2DNp.reshape((2, 4))
                        # pnp_result = PnPProcess(Point3D, Point2DNp, CamIn, CDistortCoe)
                        temp = PnPProcess(Point3D, Point2DNp, CamIn, CDistortCoe)
                        n_temp = [(temp[0] ** 2 + temp[1] ** 2) ** (1 / 2), m.atan2(temp[1], temp[0]), temp[2]]
                        # n_temp = [(CamW[0] ** 2 + CamW[1] ** 2) ** (1 / 2), m.atan2(CamW[1], CamW[0]), np.linalg.norm(RVec)]
                        pnp_result[0] = pnp_result[0] + n_temp[0]
                        pnp_result[1] = pnp_result[1] + n_temp[1]
                        pnp_result[2] = pnp_result[2] + n_temp[2]
                # pnp_result = pnp_result / count
                pnp_result[0] = pnp_result[0] / count
                pnp_result[1] = pnp_result[1] / count
                pnp_result[2] = pnp_result[2] / count

            # for num in range(num):
            # Wait for the next set of frames from the camera
            frames = pipe1.wait_for_frames()

            # Fetch pose frame
            pose = frames.get_pose_frame()
            if pose:
                data = pose.get_pose_data()
                front_data_position = data.translation
                t265_position_x = front_data_position.x

                t265_position_y = front_data_position.y

                t265_position_z = front_data_position.z

                # Print some of the pose data to the terminal

                w = data.rotation.w
                x = -data.rotation.z
                y = data.rotation.x
                z = -data.rotation.y
                pitch = -m.asin(2.0 * (x * z - w * y)) * 180.0 / m.pi
                roll = m.atan2(2.0 * (w * x + y * z), w * w - x * x - y * y + z * z) * 180.0 / m.pi
                yaw = m.atan2(2.0 * (w * z + x * y), w * w + x * x - y * y - z * z) * 180.0 / m.pi
            if len(tags) == 0:
                # print("No AprilTag detected.")
                # Last number for distinguish
                print('{} {} {} {}'.format(t265_position_z, t265_position_x, yaw, -1), end='\r')
            elif see:
                print('{} {} {} {} {} {} {}'.format(t265_position_z, t265_position_x, yaw, LandMark_result[0], LandMark_result[1], LandMark_result[2], 16), end='\r')
            else:
                print('{} {} {} {} {} {} {}'.format(t265_position_z, t265_position_x, yaw, pnp_result[0], pnp_result[1], pnp_result[2], master_numb), end='\r')

    finally:
        pipe1.stop()

if __name__ == '__main__':
    Pose()
