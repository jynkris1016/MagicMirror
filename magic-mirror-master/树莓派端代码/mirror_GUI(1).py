import tkinter as tk  # 使用Tkinter前需要先导入
import urllib.request
import urllib.error
import time
from PIL import Image,ImageTk
import cv2
import base64
import requests
import os
import pi_tryon
# import gesture
#import pyautogui
#Five Fist
# 手势识别
http_url = 'https://api-cn.faceplusplus.com/humanbodypp/v1/gesture'
key = "seZ5PM3QXjQa24MGeUui0dYs"
secret = "uwbKRrVBTZLtKS4e2UegbAWTnfVs3Pq8"


# 人脸
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
face = cv2.CascadeClassifier('C:/Users/73916/Desktop/cp-vton/haarcascade_frontalface_alt2.xml')
#face = cv2.CascadeClassifier('/home/pi/Projects/haarcascade_frontalface_alt2.xml')
#face = cv2.CascadeClassifier('./haarcascade_frontalface_alt2.xml')
#face = cv2.CascadeClassifier('D:\\desktop_document\\OpenCV\\opencv-master\\haarcascades_cuda\\haarcascade_frontalface_alt2.xml')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output1.avi', fourcc, 20.0, (640,  480))


root = tk.Tk()
root.title('My Window')
root.geometry('500x300')  # 这里的乘是小x
root.config(bg="black")

result_path="./data/test/tom_final.pth/test/try-on/result.jpg"
#result_path2="./data/test/tom_final.pth/test/try-on/result2.jpg"
body_path="./data/test/image/000010_0.jpg"
cloth_path="/home/pi/Downloads/"

text1 = "画"
im = Image.open("star.jpg")
img = ImageTk.PhotoImage(im)
l1 = tk.Label(root, text=text1, bg='black', font=('Arial', 40), fg='white', width=10, height=2)
#image = tk.Label(root, image=img)
image = tk.Label(root, image=img,width = 1000, height = 1500)
l1.pack()
image.pack()
Label1 = tk.Label(text=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), fg='white', bg='black')
Label1.pack()
im2 = Image.open(result_path)
img2 = ImageTk.PhotoImage(im2)
image2 = tk.Label(root, image=img2)
# global n
num = 0
n = 0
s_try_on = 0
cap = cv2.VideoCapture(0)
#second = gesture.sleep_time(0, 0, 1)
delay = 500

#手势 为什么one不行
#最开始显示 显示别的图
#蓝牙
#UI 星空图全屏 loading时间 返回结果换字 结果图大小 天气API 位置
#模型衣服到时候穿什么 试
#摄像头同步显示画面

def data_update():
    global text1, n, s_try_on, num,im2,img2
# time.sleep(second)
    #pyautogui.moveTo(500,500)
    ret, frame = cap.read()
    currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    Label1.config(text=currentTime)
    # face
    faces = face.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(10, 10))
    if not len(faces):
        if n >= 3:
            image2.forget()
            image.pack()
            l1.config(text="画模式")
        n = n+1
        # print(n)
    else:
        n = 0
        print(n)
        if s_try_on == 0:
            text2 = "识别到人脸，进入镜子模式"
            l1.config(text=text2)
        classname, probability = gesture_out(frame)
        print(classname)
        if probability > 0.9:
            text1 = classname

        if text1 == 'One':
            text2 = "进入试衣模式，2s后拍照"
            print("进入试衣模式，2s后拍照")
            # s_try_on=0,1,2分别代表未试衣，即将试衣，已试衣
            #if s_try_on == 1:
                #s_try_on = 2
            if s_try_on == 0:
                s_try_on = 1
            l1.config(text=text2)
            root.after(15*delay, run_try_on)
            text1 = ""
            image2.pack()

        if text1 == 'Two':
            image2.forget()
            text2 = "识别到人脸，进入镜子模式"
            print("识别到人脸，进入镜子模式")
            l1.config(text=text2)
            image2.forget()
            s_try_on = 0
            num=0

        if num == 1:
            print("num")
            print(num)
            #time.sleep(0.5)
            #im2 = Image.open(result_path)
            im2 = Image.open(result_path)
            img2 = ImageTk.PhotoImage(im2)
            image2.config(image=img2)
            #time.sleep(1)
            #image2.pack()
            root.update()
            #time.sleep(5)
            #image2.forget()
            #num = 0

        image.forget()
    # print(faces)
    #root.update()
    root.after(delay, data_update)


def run_try_on():
    print("try-on")
    global s_try_on
    if s_try_on == 1:
        s_try_on = 2
        ret, frame = cap.read()
        print("picturing")
        try_on(frame)


def try_on(frame):
    global num
    text2 = "已拍照，loading..."
    print(text2)

    l1.config(text=text2)
    root.update()
    #output_path = 'body.jpg'
    output_path = body_path
    cv2.imwrite(output_path, frame)
    num = pi_tryon.main()

# gesture
def gesture_out(frame):
    global classname_gesture, probability
    classname_gesture = ''
    probability = 0
    output_path = '1.jpg'
    cv2.imwrite(output_path, frame)
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/gesture"
    # 二进制方式打开图片文件
    f = open(output_path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = '24.d3a6d52924b37e056e690aa85992cb33.2592000.1609328494.282335-23070613'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json())
        a = response.json()
        if (int(a['result_num']) != 1):
            for i in a['result']:
                if i['classname']!= 'Face':
                    classname_gesture = i['classname']
                    probability = i['probability']
        if (int(a['result_num']) == 1):
            for i in a['result']:
                classname_gesture = i['classname']
                probability = i['probability']
    return classname_gesture, probability


root.after(delay, data_update)

root.mainloop()

