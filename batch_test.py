
import os
import pandas as pd
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import skimage.io as io
# import io as python_io
# import numpy as np
from flask import Flask, request, jsonify,Response
from flask_cors import CORS
# from PIL import Image
# import requests
import os
# from io import BytesIO
import cv2
import json
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
from datetime import datetime
import warnings
import tensorflow.python.util.deprecation as deprecation
import matplotlib.pyplot as plt
deprecation._PRINT_DEPRECATION_WARNINGS = False
# f = open('/home/ceinfo1/Desktop/10.TAB', 'r')


folder_path="/mnt/vol1/lakshya"
# folder_path1="/home/ceinfo1/Desktop/setallite_image"
# New_Tab_folder='/home/ceinfo1/Desktop/setallite_image/'

from mtcnn.mtcnn import MTCNN
warnings.filterwarnings("ignore")
# os.environ["CUDA_VISIBLE_DEVICES"]=''
net = MTCNN()

df=pd.DataFrame(columns=['image_path', 'json'])

for i in os.listdir(folder_path):
    image_path=os.path.join(folder_path,i)
    print(image_path)
    image_n= image_path.split("/")
    image_name=image_n[-1]
    #img = io.imread(image_path)
    img=cv2.imread(image_path)
    if (len(img.shape) > 3):
        img = img[:, :, :3]
    elif (len(img.shape) < 3):
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    dets = net.detect_faces(img)
    # resp = json.dumps(
    #     {'Predictions': [{'x1': i['box'][0], 'y1': i['box'][1], 'w': i['box'][2], 'h': i['box'][3]} for i in dets]})
    # print(resp)
    #print(dets[0]['box'])
    a=dets[0]['box']
    x2=a[0]+a[2]
    # print("x2",x2)
    y2=a[1]+a[3]
    # print("y2",y2)
    b=[a[0],a[1],x2,y2]
    #print("b",b)
    image=cv2.rectangle(img,(b[0],b[1]),(b[2],b[3]),(211,211,211    ),-1)
    #print(image)

    cv2.imwrite("output/"+image_name,image)
    # json=str(resp)
#     df.loc[len(df.index)] = [image_path, json]
# df.to_csv(folder_path+'/result.csv', index=False)




