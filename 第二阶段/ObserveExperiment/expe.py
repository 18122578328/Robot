from position_test_v44AprilTagPY1 import *
import numpy as np
import math


def observe(self):
    # To2到To3的变换矩阵,需要测量
    To3_o2 = np.zeros(4, 4)
    # To3到To1的变换矩阵
    To1_o3 = np.zeros(4, 4)
    # To2到To1的变换矩阵
    To1_o2 = np.zeros(4, 4)
    # 求To3到To1的变换矩阵
    for i in range(3):
        for j in range(3):
            To1_o3[i][j] = RotWCam[i][j]
    for i in range(3):
        To1_o3[i][3] = TVec[i][0]
        To1_o3[3][i] = 0
    To1_o3[3][3] = 1
    To1_o2 = np.multiply(To1_o3, To3_o2)
    return To1_o2


# 从变换矩阵得到两个机械人之间的x、y、θ的差值,返回一个数组包含这四个值
def observe_handle(self):
    # 将变换矩阵转成xyz
    x = To1_o2[0][3]
    y = To1_o2[1][3]
    # z = To1_o2[2][3]
    theta = 2*acos(CamRotQua[0, 0])
    return [x, y, theta]
