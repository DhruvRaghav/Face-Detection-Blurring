import os
import base64
import ast

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import skimage.io as io
# import io as python_io
import numpy as np
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
# from PIL import Image
# import requests
# from io import BytesIO
from flask import send_file

import blur
import cv2
import json
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
from datetime import datetime
import warnings
import tensorflow.python.util.deprecation as deprecation

deprecation._PRINT_DEPRECATION_WARNINGS = False
from gunicorn.glogging import Logger

# logging.getLogger("tensorflow.error").setLevel(logging.ERROR)
app = Flask(__name__)

if (os.path.exists('./Logs')):
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
import test

logger.propagate = False


@app.route('/blurbox', methods=['POST'])
# @cross_origin(headers=["Content-Type", "Authorization"])
def post():
    resp = Response(status=200, mimetype='application/json', content_type='application/json')

    try:

        if (request.content_type != None):

            if request.content_type.startswith('multipart/form-data'):

                if 'file' in request.files.keys():

                    if (request.files['file'].filename.endswith('.jpg')) or (
                            request.files['file'].filename.endswith('.png')):

                        file_to_predict = request.files['file']
                        # print("name", file_to_predict)
                        str_boxes = request.form['box']

                        img = io.imread(file_to_predict)
                        # print(img.shape)
                        # print(img)
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        # print(img)
                        if (len(img.shape) > 3):
                            img = img[:, :, :3]
                        elif (len(img.shape) < 3):
                            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

                        boxes = ast.literal_eval(str_boxes)

                        blur_box = blur.rectblur(img, boxes)
                        if blur_box == 'Invalid parameter':
                            return "Invalid parameter"
                        else:

                            with open("bluroutput/image.jpg", "rb") as image2string:
                                converted_string = base64.b64encode(image2string.read())
                            # print(converted_string)
                            # decodeit = open('boxblur/out.jpeg', 'wb')
                            # decodeit.write(base64.b64decode(r.text))
                            # decodeit.close()

                            return converted_string
                        # return send_file('bluroutput/image.jpg', mimetype='image/gif')
                    else:
                        resp.status_code = 400
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
        logger.error(msg=str(e), status_code=500)
        resp.status_code = 500
        return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)
