#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from __future__ import print_function
import os
import time
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import requests
import base64
from PIL import Image

#JPP
#from __future__ import print_function
from datetime import datetime
import sys
import scipy.misc
import cv2

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from JPPnet.utils import *
from JPPnet.LIP_model import *

#zhenghe.py
import json
import JPPnet_parsing

#test.py
'''import torch
import torch.nn as nn
import torch.nn.functional as F'''

'''from cp_dataset import CPDataset, CPDataLoader
from networks import GMM, UnetGenerator, load_checkpoint

from tensorboardX import SummaryWriter
from visualization import board_add_image, board_add_images, save_images'''



while True:
    time.sleep(0.1)
    if(os.path.exists("/home/ypd-24-2/DownLoad/cp-vton/data/test/cloth/004325_1.jpg")):
        if (os.path.exists("/home/ypd-24-2/DownLoad/cp-vton/data/test/image/000010_0.jpg")):
            os.system('python zhenghe.py')
            time.sleep(5)
            os.remove("/home/ypd-24-2/DownLoad/cp-vton/data/test/cloth/004325_1.jpg")
            os.remove("/home/ypd-24-2/DownLoad/cp-vton/data/test/image/000010_0.jpg")
            os.remove("/home/ypd-24-2/DownLoad/cp-vton/data/test/tom_final.pth/test/try-on/result.jpg")

