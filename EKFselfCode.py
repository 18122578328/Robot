import numpy as np
import math


# X_k（运动）和Z_k（观测距离+观测角度）是机器人自己能得到的信息,dx是个2n*1移动距离矩阵
# np.zeros创建一个矩阵，第一个参数是行，第二个参数是列
def robot_get(n):
    # 当前运动的机器人获得自己的坐标[[x1],[y1]...]，第一个下标为行，第二个下标为列，2n*1矩阵，存的机器人当前时刻的坐标（相对于起始位置）
    # 初始(x1，y1)为(0,0),之后的坐标由move指令结合计算函数得到4,n为机器人数量
    dxy = np.zeros((2 * n, 1))
    for i in range(n):
        dxy[2 * i][0] = input("input_x:")  # 第i个机器人move x
        dxy[2 * i + 1][0] = input("input_y:")  # 第i个机器人move y
    X_k = np.zeros((2 * n, 1))
    X_k += dxy
    Z_k = np.zeros((n * (n - 1), 1))
    for l in range(n - 1):
        for i in range(n - l - 1):
            temp1 = X_k[l * 2][0]  # 当前组号机器人x
            temp2 = X_k[(l + 1 + i) * 2][0]  # 被观测机器人x
            temp3 = X_k[l * 2 + 1][0]  # 当前组号机器人y
            temp4 = X_k[(l + 1 + i) * 2 + 1][0]  # 被观测机器人y
            # temp1-temp2是两个机械人之间的x的差值 temp3-temp4是两个机械人之间的y的差值
            m = (temp1 - temp2) ** 2 + (temp3 - temp4) ** 2
            o = m ** 0.5
            q = math.atan2((temp3 - temp4), (temp1 - temp2))
            Z_k[l * n - totalcount(l) + i * 2][0] = o
            Z_k[l * n - totalcount(l) + i * 2 + 1][0] = q
    return dxy, X_k, Z_k  # 2n*1的矩阵+ n(n-1)*1的矩阵


# 对X_k状态一步预测
def calc_X_now(n):  # 所有机器人同一时刻所在位置,假设只有一个机器人运动，传入move的2n*1矩阵（所有机器人下一步运动）
    dxy, X_k, Z_k = robot_get(n)
    _X_now = X_k
    return _X_now


def calcP_now(P_old, Q_old):  # 2n*2n + 2n*2n
    P_now = P_old + Q_old
    return P_now


def calcK_k(P_now, n, R_k):
    dxy, X_k, Z_k = robot_get(n)
    H_k = calcH_k(X_k, n)
    HT = np.transpose(H_k).tolist()  # 转置函数
    a = H_k @ P_now @ HT + R_k  # a,b是temp
    b = np.linalg.inv(a)  # 矩阵求逆
    K_k = P_now @ HT @ b
    return K_k


def calacZ(n, X_k):
    Z_k = np.zeros((n * (n - 1), 1))
    for l in range(n - 1):
        for i in range(n - l - 1):
            temp1 = X_k[l * 2][0]  # 当前组号机器人x
            temp2 = X_k[(l + 1 + i) * 2][0]  # 被观测机器人x
            temp3 = X_k[l * 2 + 1][0]  # 当前组号机器人y
            temp4 = X_k[(l + 1 + i) * 2 + 1][0]  # 被观测机器人y
            m = (temp1 - temp2) ** 2 + (temp3 - temp4) ** 2
            o = m ** 0.5
            q = math.atan2((temp3 - temp4), (temp1 - temp2))
            Z_k[l * n - totalcount(l) + i * 2][0] = o
            Z_k[l * n - totalcount(l) + i * 2 + 1][0] = q
            return Z_k


def calc_X_k(_X_now, K_k, Z_k, n):
    _X_now = calc_X_now(n)
    a = calacZ(n, _X_now)
    Temp_1 = Z_k - a
    Temp_2 = K_k @ Temp_1
    return _X_now + Temp_2


def calcP_k(n, K_k, H_k, P_now):
    Temp = np.eye(2 * n)
    P_k = (Temp - K_k @ H_k) @ P_now
    return P_k


def calcH_k(X_k, n):
    a = np.zeros((n * (n - 1), 2 * n))
    for l in range(n - 1):
        for i in range(n - l - 1):
            temp1 = X_k[l * 2][0]  # 当前组号机器人x
            temp2 = X_k[(l + 1 + i) * 2][0]  # 被观测机器人x
            temp3 = X_k[l * 2 + 1][0]  # 当前组号机器人y
            temp4 = X_k[(l + 1 + i) * 2 + 1][0]  # 被观测机器人y
            m = (temp1 - temp2) ** 2 + (temp3 - temp4) ** 2
            o = m ** 0.5
            a[l * n - totalcount(l) + i * 2][l * 2] = (temp1 - temp2) / o
            a[l * n - totalcount(l) + i * 2][l * 2 + 1] = (temp3 - temp4) / o
            a[l * n - totalcount(l) + i * 2][(l + i + 1) * 2] = (temp2 - temp1) / o
            a[l * n - totalcount(l) + i * 2][(l + i + 1) * 2 + 1] = (temp4 - temp3) / o
            a[l * n - totalcount(l) + i * 2 + 1][l * 2] = (temp4 - temp3) / m
            a[l * n - totalcount(l) + i * 2 + 1][l * 2 + 1] = (temp1 - temp2) / m
            a[l * n - totalcount(l) + i * 2 + 1][(l + i + 1) * 2] = (temp3 - temp4) / m
            a[l * n - totalcount(l) + i * 2 + 1][(l + i + 1) * 2 + 1] = (temp2 - temp1) / m
            return a


def totalcount(m, result=None):
    for i in range(m + 1):
        result += i
    return result


if __name__ == '__main__':
    main()
