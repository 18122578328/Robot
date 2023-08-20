import numpy as np
import pyrealsense2 as rs
import cv2
import math
import pupil_apriltags as apriltag
import sys
import os

doc = open('out.txt', 'w')
count = 10


# 相机坐标/移动坐标转到世界坐标  用变化矩阵T的逆
# RotWCam 旋转矩阵  RotCamW 旋转矩阵的转置  Jacobian  雅克比矩阵  CamRotQua相机四元素  camWR四元素转为欧拉角
def PnPProcess(Points3D, Points0, CamIn, CDistortCoe):
    # TVec位移向量 RVec旋转向量
    retval, RVec, TVec = cv2.solvePnP(Points3D, Points0, CamIn, CDistortCoe,
                                      flags=cv2.SOLVEPNP_EPNP)  # useExtrinsicGuess = False,
    RotWCam, Jacobian = cv2.Rodrigues(RVec)
    RotCamW = RotWCam.T
    CamW = np.dot(-RotCamW, TVec)

    # 四元素
    CamRotQua = np.zeros((4, 1))
    CamRotQua[0, 0] = np.sqrt(1.0 + RotWCam[0, 0] + RotWCam[1, 1] + RotWCam[2, 2]) / 2.0
    CamRotQua[1, 0] = (RotWCam[1, 2] - RotWCam[2, 1]) / (4.0 * CamRotQua[0, 0])
    CamRotQua[2, 0] = (RotWCam[2, 0] - RotWCam[0, 2]) / (4.0 * CamRotQua[0, 0])
    CamRotQua[3, 0] = (RotWCam[0, 1] - RotWCam[1, 0]) / (4.0 * CamRotQua[0, 0])

    # 四元素转为欧拉角,CamWR分别是旋转轴在xyz方向的分量，可以确定旋转轴
    CamWR = np.zeros((3, 1))
    CamWR[0, 0] = math.atan2(2.0 * (CamRotQua[0, 0] * CamRotQua[1, 0] + CamRotQua[2, 0] * CamRotQua[3, 0]),
                             1.0 - 2.0 * (CamRotQua[1, 0] * CamRotQua[1, 0] + CamRotQua[2, 0] ** 2))
    CamWR[1, 0] = math.asin(2.0 * (CamRotQua[0, 0] * CamRotQua[2, 0] - CamRotQua[3, 0] * CamRotQua[1, 0]))
    CamWR[2, 0] = math.atan2(2.0 * (CamRotQua[0, 0] * CamRotQua[3, 0] + CamRotQua[1, 0] * CamRotQua[2, 0]),
                             1.0 - 2.0 * (CamRotQua[2, 0] * CamRotQua[2, 0] + CamRotQua[3, 0] ** 2))

    CamWR = CamWR * 180.0 / math.pi
    doc = open('out.txt', 'a')
    print(CamWR)
    print(str(CamWR[0, 0]).ljust(20) + "\t" + str(CamWR[1, 0]).ljust(20) + "\t" + str(CamWR[2, 0]).ljust(20) + "\n",
          file=doc)
    doc.close()


Points3DAll = np.array([[[0, 0, 0], [0, 25, 0], [25, 25, 0], [25, 0, 0]]], dtype="double")

Points3DAllIndex = np.array([[0]])
MaxIndex = 0

Wid = 640
Hei = 480

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

while (count):

    frame = pipe.wait_for_frames()
    Color = frame.get_color_frame()
    Color_np = np.asanyarray(Color.get_data())

    Gray_np = cv2.cvtColor(Color_np, cv2.COLOR_BGR2GRAY)

    detections = apriltag.Detector(families='tag36h11', quad_decimate=2)
    tags = detections.detect(Gray_np)

    if len(tags) == 0:
        print("No AprilTag detected.")
        count = count - 1
    else:
        for tag in tags:
            ID = tag.tag_id
            print(ID)
        if ID > MaxIndex:
            print("Index out of range")
        else:
            Point2DNp = np.array(tag.corners)  ###########

            Point3D = Points3DAll[int(ID), 0:4, 0:3]
            # Point2D = Points2DNp.reshape((2, 4))
            PnPProcess(Point3D, Point2DNp, CamIn, CDistortCoe)
            count = count - 1
