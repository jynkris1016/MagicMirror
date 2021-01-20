from selenium import webdriver
import time
from PIL import Image
# 加启动配置

option = webdriver.ChromeOptions()

option.add_argument('headless')

# 打开chrome浏览器

driver = webdriver.Chrome(chrome_options=option)

driver.get("http://vs.vivo.com")

time.sleep(0)

image = driver.find_element_by_xpath('''//*[@id="loginWindow"]/div[2]/div[3]/canvas''')
#'''//*[@id="loginWindow"]/div[2]/div[3]/canvas'''

left = image.location['x']
top = image.location['y']
right = image.location['x'] + image.size['width']
bottom = image.location['y'] + image.size['height']

driver.save_screenshot("screenshot.png")  # 对整个浏览器页面进行截图

im = Image.open('screenshot.png')
im = im.crop((left, top, right, bottom))  # 对浏览器截图进行裁剪
im.save('code.png')