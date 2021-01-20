#!/usr/bin/env python
# coding: utf-8

# In[4]:


# encoding:utf-8

import requests
import base64
import os
from PIL import Image

import cv2
import numpy as np
import json
import time

import sys
sys.path.append('./JPPnet')
'''
人体关键点识别
'''

request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_analysis"
# 二进制方式打开图片文件
data_path = "./data/test/image"
file_list = os.listdir(data_path)

i = 0
for file_name in file_list:
    time.sleep(1)
    path = os.path.join(data_path, file_name)
    json_file = open(path,'rb')
    img = base64.b64encode(json_file.read())
    print("ok")
    params = {"image":img}
    access_token = '24.0b5861b262e270b2c2605f8827ab9412.2592000.1608728970.282335-22991921'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)

    a = response.json()
    b=['nose','neck','right_shoulder','right_elbow','right_wrist','left_shoulder','left_elbow','left_wrist','right_hip','right_knee','right_ankle','left_hip','left_knee','left_ankle','right_eye','left_eye','right_ear','left_ear']
    c=[]
    for i in b:
            c.append(a['person_info'][0]['body_parts'][i]['x'])
            c.append(a['person_info'][0]['body_parts'][i]['y'])
            c.append(a['person_info'][0]['body_parts'][i]['score'])
    openpose={}
    openpose={"people":[{"pose_keypoints":c}]}
    file_name = file_name.split('.')[0]
    path = './data/test/pose/' + file_name + "_keypoints.json"
    with open(path, 'w') as json_file:
        json.dump(openpose,json_file)


# In[7]:


#获取灰度图蒙版
data_path = "data/test/cloth/"
file_list = os.listdir(data_path)
i = 0
for file in file_list:
    path = os.path.join(data_path, file)
    img=cv2.imread(path)

    img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    ret,thresh2 = cv2.threshold(img_gray, 245, 255, cv2.THRESH_BINARY_INV)  # （黑白二值反转）
    save_path = './data/test/cloth-mask/' + file
    cv2.imwrite(save_path, thresh2)


# In[2]:


# 使用JPPNET生成解析图像

from JPPnet import JPPnet_parsing
# In[3]:
print("JPP begin ! ! ")

JPPnet_parsing.main()


# In[6]:
data_path = "data/test/image-parse"
file_list = os.listdir(data_path)
print(file_list)
i = 0
for file_name in file_list:
    path = os.path.join(data_path, file_name)
    img = Image.open(path)
    img = img.convert("P")

    img_array = np.array(img)
    img_array.dtype
    
    print(file_name)
    img.save("./data/test/image-parse/" + file_name)


# In[7]:


# 运行GMM模型
os.system('python3 test.py --name gmm_traintest_new --stage GMM --workers 4 --datamode test --data_list test_pairs.txt --checkpoint checkpoints/gmm_final.pth')
# In[8]:

# 运行try_on模型
os.system('python3 test.py --name tom_test_new --stage TOM --workers 4 --datamode test --data_list test_pairs.txt --checkpoint checkpoints/tom_final.pth')


# In[25]:


from PIL import Image
parse = Image.open('./data/test/image-parse/000010_0.png')
image_good = Image.open('./data/test/image/000010_0.jpg')
image = Image.open('./data/test/tom_final.pth/test/try-on/000010_0.jpg')
rgb_parse = parse.convert('RGB')
rgb_image = image.convert('RGB')
rgb_good = image_good.convert('RGB')
for i in range(192):
    for j in range(256):
        r, g, b = rgb_parse.getpixel((i, j))
        if(r==255):
            if(g==0):
                r1,g1,b1 = rgb_good.getpixel((i,j))
                rgb_image.putpixel((i,j),(r1,g1,b1))
        elif(g==0):
            if(b==255):
                r1,g1,b1 = rgb_good.getpixel((i,j))
                rgb_image.putpixel((i,j),(r1,g1,b1))
            elif(b==0):
                r1,g1,b1 = rgb_good.getpixel((i,j))
                rgb_image.putpixel((i,j),(r1,g1,b1))
rgb_image.save("./data/test/tom_final.pth/test/try-on/result.jpg")