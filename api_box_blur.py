import os
import base64

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import skimage.io as io

from flask import Flask, request, jsonify, Response
from flask_cors import CORS

import cv2

import logging

from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
from datetime import datetime

import tensorflow.python.util.deprecation as deprecation

deprecation._PRINT_DEPRECATION_WARNINGS = False

app = Flask(__name__)

if (os.path.exists('./Logs')):
    os.makedirs('./Logs', exist_ok=True)
logger = logging.getLogger('gunicorn.workers')

log_filename = datetime.now().strftime('%Y-%m-%d') + '.log'
handler = TimedRotatingFileHandler('Logs/' + log_filename, when='MIDNIGHT', backupCount=7)
formatter = Formatter(fmt='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%d-%m-%Y %I:%M:%S %p')

logger.setLevel(logger.level)

handler.setLevel(logging.INFO)

handler.setFormatter(formatter)

logger.addHandler(handler)

logger.propagate = False


@app.route('/boxblur', methods=['POST'])
def boxbluring():
    # resp = Response(status=200, mimetype='application/json', content_type='application/json')
    if request.method != 'POST':
    # try:
        # if (request.content_type != None):
        # if request.content_type.startswith('multipart/form-data'):
        # if 'file' in request.files.keys():
        # if (request.files['file'].filename.endswith('.jpg')) or (
        #         request.files['file'].filename.endswith('.png')):
        file_to_predict = request.files['file']
        box = request.form['box']
        print(box)

        return 'hi'
    # except:
    #     return 'Not found'


# CORS(app, supports_credentials=True, allow_headers=['Content-Type', 'X-ACCESS_TOKEN', 'Authorization'])
# application = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=False)
