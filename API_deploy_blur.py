import os
import gc
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import skimage.io as io
# import io as python_io
# import numpy as np
from flask import Flask, request, jsonify,Response
from flask_cors import CORS
from flask import send_file
from PIL import Image
import requests
from io import BytesIO
import base64
import cv2
import json
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
from datetime import datetime
import warnings
import blur
import tensorflow.python.util.deprecation as deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False
from gunicorn.glogging import Logger
# logging.getLogger("tensorflow.error").setLevel(logging.ERROR)
app = Flask(__name__)



if(os.path.exists('./Logs')):
    os.makedirs('./Logs', exist_ok=True)
logger = logging.getLogger('gunicorn.workers')

# logger = logging.getLogger('gunicorn')
# logger = logging.getLogger('__name__')
log_filename = datetime.now().strftime('%Y-%m-%d') + '.log'
handler = TimedRotatingFileHandler('Logs/' + log_filename, when='MIDNIGHT', backupCount=7)
formatter = Formatter(fmt='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%d-%m-%Y %I:%M:%S %p')

logger.setLevel(logger.level)
# app.logger.handlers = logger.handlers
# app.logger.setLevel(logger.level)
handler.setLevel(logging.INFO)
# handler.setStream(logging.StreamHandler)
handler.setFormatter(formatter)

# logger.setLevel(logging.INFO)
logger.addHandler(handler)

logger.propagate = False

#call mtcnn model constructor
try:
    from mtcnn.mtcnn import MTCNN
    warnings.filterwarnings("ignore")
    # os.environ["CUDA_VISIBLE_DEVICES"]=''
    net = MTCNN()
except Warning as e:
    logger.info(str(e))
# @app.route('/')
# def welcome():
#     return('''
#     --------WELCOME TO FACE DETECTION MICROSERVICE------''')

@app.route('/facedetection', methods=['POST'])
# @cross_origin(headers=["Content-Type", "Authorization"])
def post():
    # print("Processing Face Detection API request")
    # if request.content_type.startswith('multipart/form-data'):
    #     request_data = request.form.to_dict()
    # img = request.file.get('image')
        #errors = []
       # if 'file' not in request.files:
          #  errors.append({'file': 'please provide file'})
    resp = Response(status=200, mimetype='application/json',content_type='application/json')
    # print(request.host,request.url)
    # print(request.content_type)
    try:
        if(request.content_type!=None):
            if request.content_type.startswith('multipart/form-data'):
                if 'file' in request.files.keys():
                    if(request.files['file'].filename.endswith('.jpg')):
                        file_to_predict = request.files['file']
                        img = io.imread(file_to_predict)
                        if(len(img.shape)>3):
                                img=img[:,:,:3]
                        elif(len(img.shape)<3):
                                img=cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
                        dets = net.detect_faces(img)
                        # print('dets',dets)
                        # resp=json.dumps({'Predictions':[{'x1':i['box'][0],'y1':i['box'][1],'w':i['box'][2],'h':i['box'][3]} for i in dets]})
                        boxes = [x['box'] for x in dets]

                        blur_img = blur.blur(img,boxes)

                        print(blur_img.shape)
                        # return jsonify({'msg':'success','size':[blur_img.shape[1], blur_img.shape[0]]})
                        # gc.collect()

                        return send_file('output/image.jpg', mimetype='image/gif')
                        # return f'<img src = "data:image/png;base64,{data}">'
                    else:
                        resp.status_code=400
                        return resp
                else:
                    resp.status_code = 400
                    return resp
            else:
                resp.status_code = 400
                return resp
        else:
            resp.status_code = 400
            return resp
    except Exception as e:
        logger.error(msg=str(e),status_code=500)
        resp.status_code=500
        return resp



CORS(app, supports_credentials=True, allow_headers=['Content-Type', 'X-ACCESS_TOKEN', 'Authorization'])
# application = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=False)
