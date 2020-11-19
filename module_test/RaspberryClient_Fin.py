#!/usr/bin/env python
# -*- coding=utf-8 -*-

import socket
import os
import sys
import struct

def Status_Raspberry():
    #这里获取状态代码（闲置、上传图片、分类信息）拍好照STATUS改为01
    STATUS = '01'
    # '00'闲置 '01'上传图片 '02'分类信息
    return STATUS

def socket_client(STATUS,MESSAGE = ''):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '8.129.109.115'
        port = 9999
        s.connect((host, port))
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    if STATUS == '00':
        s.sendall(STATUS.encode('utf-8'))
        answer = s.recv(1024).decode('utf-8')
        if answer == 'GOTCHA':
            s.sendall('OK'.encode('utf-8'))
            answer == s.recv(1024).decode('utf-8')
            if answer =='ShowMePhoto':
                ###########让树莓派拍照############拍完STATUS改为01
                pass
            elif answer =='Nothing':
                pass

        ############还要发送机器信息

        s.close
    elif STATUS == '01':
        s.sendall(STATUS.encode('utf-8'))
        answer = s.recv(1024).decode('utf-8')
        if answer == 'GOTCHA':
            print(answer)
            while 1:
                filepath = 'image.jpg'#############test
                if os.path.isfile(filepath):
                    # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
                    fileinfo_size = struct.calcsize('128sl')
                    # 定义文件头信息，包含文件名和文件大小
                    fhead = struct.pack('128sl', bytes(os.path.basename(filepath).encode('utf-8')),os.stat(filepath).st_size)
                    s.send(fhead)
                    print ('client filepath: {0}'.format(filepath))
                    fp = open(filepath, 'rb')
                    while 1:
                        data = fp.read(1024)
                        if not data:
                            print ('{0} file send over...'.format(filepath))
                            break
                        s.send(data)
                s.close()
                break
    elif STATUS == '02':
        s.sendall(STATUS.encode('utf-8'))
        answer = s.recv(1024).decode('utf-8')
        if answer == 'GOTCHA':
            s.sendall(MESSAGE.encode('utf-8'))
            #MESSAGE格式：种类(recyclable,dry,wet,harmful)例：recyclable
        s.close()

if __name__ == '__main__':
    STATUS = Status_Raspberry()
    MESSAGE = 'recyclable'#test这里是垃圾种类
    socket_client(STATUS,MESSAGE)