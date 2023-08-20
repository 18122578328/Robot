experimentCode
experimentCode是用于求解直线运动中的∆D以及∆Θ
distance_array，即∆D，是move前、后两点间距离，是通过将move前、后的data.translation里的x、y提取出来后由勾股定理计算得出。即(∆x*∆x+∆y*∆y)开根号。该数据将会被储存至distance_data.txt文件里。

angle_array是move前、后两点间直线与move前的运动方向的夹角，由arctan(∆y/∆x)得出，单位是弧度。该数据被储存至angle_data.txt文件里。
experimentCode2
experimentCode2用于求解旋转中的∆Θ
yaw是move z 前后的角度之差，单位是度。该数据被储存至yaw_angle_data.txt文件里。

想要更改实验次数，只需更改for循环里的range