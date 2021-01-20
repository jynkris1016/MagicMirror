#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import time
while True:
    time.sleep(0.1)
    if(os.path.exists("/home/ypd-24-2/DownLoad/cp-vton/data/test/cloth/004325_1.jpg")):
        if (os.path.exists("/home/ypd-24-2/DownLoad/cp-vton/data/test/image/000010_0.jpg")):
            os.system('python zhenghe.py')
            time.sleep(1)
            os.remove("/home/ypd-24-2/DownLoad/cp-vton/data/test/cloth/004325_1.jpg")
            os.remove("/home/ypd-24-2/DownLoad/cp-vton/data/test/image/000010_0.jpg")
        #os.remove("/home/ypd-24-2/DownLoad/cp-vton/data/test/tom_final.pth/test/try-on/result.jpg")

