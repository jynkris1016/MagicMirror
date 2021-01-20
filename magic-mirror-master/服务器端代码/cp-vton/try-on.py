#!/usr/bin/env python
# coding: utf-8

# In[3]:


import paramiko  # 用于调用scp命令
from scp import SCPClient
import os
import time
from PIL import Image
import numpy as np


def ssh_scp_put(ip, username, password, local_file, remote_path):

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(hostname=str(ip), port=22, username=username, password=password)

    scp = SCPClient(ssh.get_transport())
    scp.put(local_file, recursive=True, remote_path=remote_path)
    scp.close()


def remote_scp(host_ip, remote_path, local_path, username, password):
    try:
        t = paramiko.Transport((host_ip, 22))
        t.connect(username=username, password=password) # 登录远程服务器
        sftp = paramiko.SFTPClient.from_transport(t) # sftp传输协议
        src = remote_path
        des = local_path
        sftp.get(src, des) #下载文件
        # sftp.put(updatepath_file(),src) #上传文件
        t.close()
        #return True # 因为服务器上只能覆盖，不能新生成文件，所以文件一定存在，没有必要设置返回值
        
    except IOError as e:
        print(e)
        #return False


def main():
    ip = "10.110.210.24"
    username = "ypd-24-2"
    password = "ypd-24-2"

    local_up1 = "./data/test/cloth/004325_1.jpg"
    remote_up1 = "/home/ypd-24-2/DownLoad/cp-vton/data/test/cloth/004325_1.jpg"
    local_up2 = "./data/test/image/000010_0.jpg"
    remote_up2 = "/home/ypd-24-2/DownLoad/cp-vton/data/test/image/000010_0.jpg"
    local_down = "./data/test/tom_final.pth/test/try-on/result.jpg"
    remote_down = "/home/ypd-24-2/DownLoad/cp-vton/data/test/tom_final.pth/test/try-on/result.jpg"

    c = 0
    num = 0 # 不显示服务器上原始空result图像
    rootdir = "/home/pi/Downloads/"#树莓派蓝牙文件夹 提前随便存一个文件
    while True:
        time.sleep(0.1)
        list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
        if len(list)==2:
            for i in range(2):
                path = os.path.join(rootdir,list[i])
                file=os.path.splitext(path)
                filename,type=file
                if type==".jpg":
                    cloth_path = path
                    print(path)
                    break
            cloth_file = Image.open(cloth_path)     
            print(cloth_file.size)        
            x_s = 192 
            y_s = 256 
            cloth_out = cloth_file.resize((x_s,y_s),Image.ANTIALIAS) 
            cloth_out.save('./data/test/cloth/004325_1.jpg')
            print(cloth_out.size)
            os.remove(cloth_path)
        a = os.path.exists(local_up1)
        b = os.path.exists(local_up2)
        
        if (a):
            if (b):
                image_file = Image.open('/media/pi/F4AE-07BC/cp-vton/data/test/image/000010_0.jpg')
                x_s = 192 
                y_s = 256         
                image_out = image_file.resize((x_s,y_s),Image.ANTIALIAS) 
                image_out.save('/media/pi/F4AE-07BC/cp-vton/data/test/image/000010_0.jpg')
                print("ok")
                ssh_scp_put(ip, username, password, local_up1, remote_up1)
                print("finished up1")
                ssh_scp_put(ip, username, password, local_up2, remote_up2)
                print("finished up2")
                os.remove(local_up1)
                os.remove(local_up2)  # 下载新图片之后，删除原始衣物和人像图片，等待下一次上行
                # 上传之后就一直监听，直到result更新
                #remote_scp(ip, remote_down, local_down, username, password)
        c0 = os.path.getmtime(local_down)  # 读取新下载下来的图像时间
        if (c0 != c): # 也就是result更新了
            print("gengxin")
                    if(num):
                        remote_scp(ip, remote_down, local_down, username, password)
                        print("finished down")
                        c = os.path.getmtime(local_down) # 更新result时间信息（这样比再读一次快？）
                    num = 1
                    

        '''c0 = os.path.getmtime(local_down)
        #print(c0)
        if (c0 != c):
            num += 1
            if(num):
                remote_scp(ip, remote_down, local_down, username, password)
            #if ((remote_scp(ip, remote_down, local_down, username, password))):
                c = os.path.getmtime(local_down)
                print("finished down")
                os.remove(local_up1)
                os.remove(local_up2)'''


if __name__ == '__main__':
    main()
    '''ip = "10.110.210.24"
    username = "ypd-24-2"
    password = "ypd-24-2"

    local_up1 = "./data/test/cloth/004325_1.jpg"
    remote_up1 = "/home/ypd-24-2/DownLoad/cp-vton/data/test/cloth/004325_1.jpg"
    local_up2 = "./data/test/image/000010_0.jpg"
    remote_up2 = "/home/ypd-24-2/DownLoad/cp-vton/data/test/image/000010_0.jpg"
    local_down = "./data/test/tom_final.pth/test/try-on/result.jpg"
    remote_down = "/home/ypd-24-2/DownLoad/cp-vton/data/test/tom_final.pth/test/try-on/result.jpg"'''

#     ssh_scp_put(ip, username, password, local_up, remote_up)
#     print("finished up")
#     remote_scp(ip, remote_down, local_down, username, password)
#     print("finished down")


# In[ ]:



'''c = 0
while True:
    time.sleep(0.1)
    a = os.path.exists(local_up1)
    b = os.path.exists(local_up2)
    if(a):
        if(b):
            ssh_scp_put(ip, username, password, local_up1, remote_up1)
            print("finished up1")
            ssh_scp_put(ip, username, password, local_up2, remote_up2)
            print("finished up2")
            os.remove(local_up1)
            os.remove(local_up2)
    c0 = os.path.getmtime(local_down)
    print(c0)
    if(c0!=c):
        if((remote_scp(ip, remote_down, local_down, username, password))):
            c = os.path.getmtime(local_down)
            print("finished down")
'''

# In[ ]:




