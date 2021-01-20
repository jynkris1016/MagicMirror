'''#手势 为什么one不行
    识别的可信度设置得太高
#最开始显示 显示别的图
    已解决，
    但是现在拍一张之后必须退出到镜子模式，不能重复合成
    上面那个可以了，比划2进入试衣模式即可
#蓝牙
    改成互传，访问浏览器还没有解决
    访问浏览器保存二维码截图之后的逻辑问题
#UI 星空图全屏 loading时间 返回结果换字 结果图大小 天气API 位置
    星空图基本全屏，上面还有一条lable，大小调成0也不行??????
    换字已解决
    结果图大小已调整
    loading的时候写了lable1.forget，但是不知道为啥不消失，调试到那句的时候没有任何反应??????
    label1.forget已解决，没有更新
    现在还需要在运行try-on的时候更新界面，使用全局变量
#模型衣服到时候穿什么 试
#摄像头同步显示画面'''

import global_data
import tkinter as tk  # 使用Tkinter前需要先导入
import time
from PIL import Image,ImageTk
import cv2
import base64
import requests
import os
import pi_tryon
import json
from selenium import webdriver
from selenium.webdriver import Chrome

root = tk.Tk()

#连接浏览器
if (global_data.code_num == 0):
        download_location = '/home/pi/Downloads'
        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': download_location,
                 'download.prompt_for_download': False,
                 'download.directory_upgrade': True,
                 'safebrowsing.enabled': False,
                 'safebrowsing.disable_download_protection': True}

        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument("--headless")
        driver = Chrome(chrome_options=chrome_options)
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_location}}
        command_result = driver.execute("send_command", params)
        print("response from browser:")
        for key in command_result:
            print("result:" + key + ":" + str(command_result[key]))

        driver.minimize_window()

        driver.get("http:\\vs.vivo.com")
        time.sleep(5)
        image = driver.find_element_by_id("loginWindow")
        print("ok")

        left = image.location['x']
        top = image.location['y']
        right = image.location['x'] + image.size['width']
        bottom = image.location['y'] + image.size['height']

        driver.save_screenshot("screenshot.png")  # 对整个浏览器页面进行截图
        im = Image.open('screenshot.png')
        im = im.crop((left, top, right, bottom))  # 对浏览器截图进行裁剪

        im.save('code.png')
        print('save')
        code = Image.open("code.png")

        code_new = code.resize((720, 540), Image.ANTIALIAS)
        code_new.save("code.png")



star_file = Image.open("star.jpg")
print(star_file.size)
#这里的宽高尺寸需要等屏幕到了调试一下，只改这里就行，后面都是按比例设置的
star_width = 800
star_height = 480
star_out = star_file.resize((star_width, star_height), Image.ANTIALIAS)
star_out.save("star.jpg")
# 手势识别
http_url = 'https://api-cn.faceplusplus.com/humanbodypp/v1/gesture'
key = "seZ5PM3QXjQa24MGeUui0dYs"
secret = "uwbKRrVBTZLtKS4e2UegbAWTnfVs3Pq8"
#调取天气
weatherJsonUrl = "http://wthrcdn.etouch.cn/weather_mini?city=北京"  # 将链接定义为一个字符串
response = requests.get(weatherJsonUrl)  # 获取并下载页面，其内容会保存在respons.text成员变量里面
response.raise_for_status()  # 这句代码的意思如果请求失败的话就会抛出异常，请求正常就上面也不会做
# 将json文件格式导入成python的格式
weatherData = json.loads(response.text)

# 人脸

#face = cv2.CascadeClassifier('C:/Users/73916/Desktop/cp-vton/haarcascade_frontalface_alt2.xml')
#face = cv2.CascadeClassifier('D:/Download/cp-vton/haarcascade_frontalface_alt2.xml')
face = cv2.CascadeClassifier('/home/pi/Projects/haarcascade_frontalface_alt2.xml')
#face = cv2.CascadeClassifier('D:\\desktop_document\\OpenCV\\opencv-master\\haarcascades_cuda\\haarcascade_frontalface_alt2.xml')


#root.title('Welcome to Magic Mirror')
#root.geometry('500x300')  # 这里的乘是小x
#root.geometry('1000x500')
root.geometry(str(star_width)+"x"+str(star_height))
root.config(bg="black")

result_path="./data/test/tom_final.pth/test/try-on/result.jpg"
#result_path2="./data/test/tom_final.pth/test/try-on/result2.jpg"
body_path="./data/test/image/000010_0.jpg"
#cloth_path="/home/pi/Downloads/"

text1 = "无人状态"
im = Image.open("star.jpg")
img = ImageTk.PhotoImage(im)
#l1 = tk.Label(root, text=text1, bg='black', font=('Arial', 20), fg='white', width=4, height=2)
l1 = tk.Label(root, text=text1, bg='black', font=('楷体', 15), fg='white')
#image = tk.Label(root, image=img)
image = tk.Label(root, image=img,bg='black',width = star_width, height = star_height)
#l1.pack()  #l1是状态标签
image.pack()

#时间
time_label = tk.Label(text=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),  font = (10),fg='white', bg='black')
#Label1.pack()

weather_json = ""
weather_json += str(weatherData['data']['forecast'][0]['high'])+"   "
weather_json += str(weatherData['data']['forecast'][0]['low'])+"   "
weather_json += str(weatherData['data']['forecast'][0]['type'])+"   "
weather_json += str(weatherData['data']['forecast'][0]['fengxiang'])+"   "
print(weather_json)
suggest = str(weatherData['data']['ganmao'])
print(suggest)
weather = tk.Label(root, text=weather_json, bg='black', font=('楷体', 13), fg='white')
suggestion = tk.Label(root, text=suggest, bg='black', font=('楷体', 13), fg='white')


'''im2 = Image.open(result_path)
img2 = ImageTk.PhotoImage(im2)

star_file = Image.open("star.jpg")
print(star_file.size)
#这里的宽高尺寸需要等屏幕到了调试一下，只改这里就行，后面都是按比例设置的
star_width = 800
star_height = 480
star_out = star_file.resize((star_width, star_height), Image.ANTIALIAS)
star_out.save("star.jpg")
im = Image.open("star.jpg")
img = ImageTk.PhotoImage(im)
#l1 = tk.Label(root, text=text1, bg='black', font=('Arial', 20), fg='white', width=4, height=2)
l1 = tk.Label(root, text=text1, bg='black', font=('楷体', 15), fg='white')
#image = tk.Label(root, image=img)
image = tk.Label(root, image=img,bg='black',width = star_width, height = star_height)
#l1.pack()  #l1是状态标签
image.pack()
'''

im2_file = Image.open(result_path)
im2_out = star_file.resize((300, 400), Image.ANTIALIAS)
im2_out.save(result_path)

im2 = Image.open(result_path)
img2 = ImageTk.PhotoImage(im2)
image2 = tk.Label(root, image=img2, width = 300,height = 400)
#image2 = tk.Label(root, image=img2, width = 300,height = 400)
# global ntk.Label
num = 0
global_data.code_num = 0   #是否为第一次没有扫过二维码
n = 0
s_try_on = 0
cap = cv2.VideoCapture(0)
#second = gesture.sleep_time(0, 0, 1)
delay = 500



def data_update():
    global text1, n, s_try_on, num,im2,img2
# time.sleep(second)
    #pyautogui.moveTo(500,500)
    ret, frame = cap.read()
    currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  #获取时间，每秒刷新一次
    time_label.config(text=currentTime)
    # face
    faces = face.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(10, 10))
    if not len(faces):
        if n >= 3:
            image2.forget()
            image.pack()
            l1.forget()   #l1是状态标签，label1是时间
            time_label.forget()
            weather.forget()
            suggestion.forget()
            s_try_on = 0
            num = 0
            #l1.config(text="无人状态", width=0, height=0)
        n = n+1
        # print(n)
    else:
        n = 0
        print(n)
        if s_try_on == 0:
            text2 = "识别到人脸，进入镜子模式"
            l1.config(text=text2,width=30, height=2)
            l1.pack()
            time_label.pack()
            weather.pack()
            suggestion.pack()
            image2.forget()
            #root.update()

        classname, probability = gesture_out(frame)
        if probability > 0.5:
            text1 = classname   #classname为手势识别结果
			#print(classname)
       

        image.forget()

        # 新版
        if (text1 == 'Fist') and (s_try_on ==0):
        #if text1 == 'Fist':
            s_try_on = 1
            num = 0
            print("进入试衣模式，5s后拍照")


        if text1 == 'Five':
            #text2 = "识别到人脸，进入镜子模式"
            print("退出试衣模式")
            #l1.config(text=text2, width=30, height=2)
            #image2.forget()
            s_try_on = 0
            num = 0

        if s_try_on == 1 :
            image2.forget()
            text2 = "进入试衣模式，5s后拍照"
            l1.config(text=text2, width=30, height=2)
            s_try_on = 2
            root.after(15 * delay, run_try_on)


        if s_try_on == 2:
            #image2.forget()
            text2 = "进入试衣模式，5s后拍照"
            l1.config(text=text2, width=30, height=2)
            time_label.pack()
            weather.pack()
            suggestion.pack()
            image2.forget()
            #root.update()

        if num == 1:
            # image_code.forget()
            #s_try_on=0
            text2 = "感谢等待，试衣效果图如下"
            print("num")
            print(num)
            # time.sleep(0.5)
            # im2 = Image.open(result_path)
            im2 = Image.open(result_path)
            img2 = ImageTk.PhotoImage(im2)
            image2.config(image=img2)
            # time.sleep(1)
            time_label.forget()
            weather.forget()
            suggestion.forget()
            image2.pack()
            # text2 = "感谢等待，试衣效果图如下"
            global_data.code_num = 1
            print(text2)
            l1.config(text=text2, width=30, height=2)
            #image2.pack()
            # root.update()

            root.update()

    # print(faces)
    #root.update()
    root.after(delay, data_update)


def run_try_on():
    print("try-on")
    global s_try_on
    # 旧
    '''if s_try_on == 1:
        s_try_on = 2
        ret, frame = cap.read()
        print("picturing")
        try_on(frame)'''
    # 新
    ret, frame = cap.read()
    print("picturing")
    try_on(frame)


def try_on(frame):
    global num
    text2 = "已拍照，请上传图片"
    print(text2)
    if (global_data.code_num == 0):
        code = Image.open("code.png")

        code_new = code.resize((720, 540), Image.ANTIALIAS)
        code_new.save("code.png")
        code = Image.open("code.png")

        img_code = ImageTk.PhotoImage(code)
        image_code = tk.Label(root, image=img_code,bg='black',width = 720, height = 540)
        image_code.pack()
        #
        text2 = "已拍照，请扫码上传图片"
        #codenum = 1

    #ret, frame = cap.read()
    l1.config(text=text2, width=30, height=2)
    root.update()
    #output_path = 'body.jpg'
    output_path = body_path
    cv2.imwrite(output_path, frame)
    time_label.forget()
    weather.forget()
    suggestion.forget()

    root.update()

    num = pi_tryon.main()
    #global_data.code_num = 1

    '''time_label.pack()
    weather.pack()
    suggestion.pack()'''
    if (global_data.code_num == 0):
        image_code.forget()
    root.update()

'''    text2 = "感谢等待，试衣效果图如下"
    global_data.code_num = 1
    print(text2)
    l1.config(text=text2, width=30, height=2)
    image2.pack()
    root.update()'''

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

