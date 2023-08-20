# -*- coding: utf-8 -*-
import time

import pexpect
from pexpect import pxssh
# import common
import sys
from temp import tag1

password = "nano"

class pi_mgr(object):

    # 类变量包括 mac2ip ip2mac ssh_dct[mac]=ssh
    def __init__(self, mac2ip, ip2mac):
        self.mac2ip = mac2ip
        self.ip2mac = ip2mac
        ssh_dct = dict()
        for mac, ip in mac2ip.items():
            # 实例化pxssh对象
            ssh = pxssh.pxssh()
            # 登录
            ssh.login(ip, "nano", password)
            ssh_dct[mac] = ssh
            ssh.sendline("cd test_li")
            ssh.sendline("conda activate CL")
            # 匹配prompt(提示符)
            ssh.prompt()
            mess = ssh.before
            # print(mess)
        self.ssh_dct = ssh_dct

    # 运行pi.py
    def launch(self, name="temp.py"):
        for ssh in self.ssh_dct.values():
            ssh.sendline(f"python3 {name}")
            
    def get_output(self):
        for ssh in self.ssh_dct.values():
            # 匹配prompt(提示符)
            ssh.prompt()
            mes1 = ssh.before
            ssh.prompt()
            mes = ssh.before
            mes = str(mes)
            print(mes)
            mes_list = mes.split('\\r\\n')
            mes_list = mes_list[1].split('\\r')
            print(mes_list)
            message = mes_list[1]
            print(message)
            # print(mes_list)
            temp = message.split(' ')
            temp1 = []
            for t in temp:
                if t != '':
                    temp1.append(t)
            # if len(temp1) > 3:
            #     t265x = temp1[0]
            #     t265y = temp1[1]
            #     t265z = temp1[2]
            #     CamW0 = temp1[3]
            #     CamW1 = temp1[4]
            #     CamW2 = temp1[5]
            #     Rvec0 = temp1[6]
            #     Rvec1 = temp1[7]
            #     Rvec2 = temp1[8]
            # else:
            #     t265x = temp1[0]
            #     t265y = temp1[1]
            #     t265z = temp1[2]
            return temp1
            
    # 退出ssh
    def logout(self):
        for ssh in self.ssh_dct.values():
            ssh.logout()


if __name__ == '__main__':
    mac2ip = dict()
    ip2mac = dict()
    mac2ip['08:be:ac:2c:ad:5b'] = '192.168.39.166'
    ip2mac['192.168.39.166'] = '08:be:ac:2c:ad:5b'
    nano1 = pi_mgr(mac2ip, ip2mac)
    nano1.launch("temp.py")
    # nano1.logout()
