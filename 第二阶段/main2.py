import sys
import time
import threading
import socket
import numpy as np
import math
import EKF

IP_LIST = []
EP_DICT = {}
start_POSITION=np.array()
get_POSITION=np.zeros((3n,1))             #获取的各机器人位置信息矩阵x，y，z
now_POSITION=np.zeros((3n,1))
A=np.ones((n,n))                        #A矩阵假设，全1矩阵

#获取各机器人位置信息
def getPOSITION():
        k=0
        for ip in IP_LIST:
                EP_DICT[ip].command('chassis position ?')
                buf = s.recv(1024)
                position=buf.decode('utf-8')
                position=position.split(",")
                get_POSITION[k,0]=float(position[0])
                get_POSITION[k+1,0] = float(position[1])
                get_POSITION[k+2,0] = float(position[2])
                now_POSITION[k,0] = start_POSITION[ip][1] + get_POSITION[k,0] * math.cos(start_POSITION[ip][3] * math.py / 180) - get_POSITION[k,0] * math.sin(start_POSITION[ip][3] * math.py / 180)
                now_POSITION[k+1, 0] = start_POSITION[ip][2]+get_POSITION[k+1,0]*math.sin(start_POSITION[ip][3]*math.py/180)+get_POSITION[k+1,0]*math.cos(start_POSITION[ip][3]*math.py/180)
                now_POSITION[k+2,0] = start_POSITION[ip][3] + get_POSITION[k+2,0]
                k=k+3
        return now_POSITION


#P_old_xz,Q_xz,R_k,X_old_xz,z，P_old_zz, Q_zz, X_old_zz, D为手动输入的数值

final_Xk_xz,P_k_xz=EKF.final_xz(getPOSITION(),P_old_xz,Q_xz,R_k,X_old_xz,z)                             #旋转卡尔曼滤波
time.sleep(5)
final_Xk_zz,P_k_zz=EKF.final_zz(R_k,getPOSITION(), P_old_zz, Q_zz, X_old_zz, D,final_Xk_xz)             #直走卡尔曼滤波
