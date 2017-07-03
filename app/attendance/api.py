# -*- coding: utf-8 -*-
"""
Created on Sat Jul 01 10:00:31 2017

@author: wanggd
"""

import requests
import os 
import mimetypes
import cv2


API_KEY = '7czGl-WWMO88mUMjMXspnKFL6rQIuCp4'
API_SECRET = 's9EJmZhlK3X84EtbKzv5V7Nh0TKFda7p'
face_set_token = u'7762386b14d65571266c05a5edd2f630'

faceCascade = cv2.CascadeClassifier('./features/haarcascade_frontalface_default.xml')


def get_response(img_path1, img_path2):
         
    BASE_URL = 'https://api-cn.faceplusplus.com/facepp/v3/compare' 
    
    data = {'api_key': API_KEY,
            'api_secret': API_SECRET}
    
    try:
        files = {'image_file1': (os.path.basename(img_path1), open(img_path1, 'rb'),
                mimetypes.guess_type(img_path1)[0]), 
                 'image_file2': (os.path.basename(img_path2), open(img_path2, 'rb'),
                mimetypes.guess_type(img_path2)[0])}
                
        if not detect_face(img_path1) or not detect_face(img_path2):
            raise ValueError('No face detected') 
    
        return requests.post(BASE_URL, files = files, data = data).json()
    except:
        print('尚未收集您的照片')
    
    
    
def detect_face(img):
    if isinstance(img, str):
        img = cv2.imread(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = faceCascade.detectMultiScale(gray, 1.3, 5)
    return len(face) != 0