#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 21:20:11 2017

@author: wanggd
"""

import requests
import os 
import mimetypes
import cv2
import time
from django.conf import settings

API_KEY = '7czGl-WWMO88mUMjMXspnKFL6rQIuCp4'
API_SECRET = 's9EJmZhlK3X84EtbKzv5V7Nh0TKFda7p'

faceCascade = cv2.CascadeClassifier('./features/haarcascade_frontalface_default.xml')

 
def check(img_path1, img_path2):
    return get_response(img_path1, img_path2)['confidence'] > 90

def detect_face(img):
    if isinstance(img, str):
        img = cv2.imread(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = faceCascade.detectMultiScale(gray, 1.3, 5)
    return len(face) != 0

def get_response(img_path1, img_path2):
    
    BASE_URL = 'https://api-cn.faceplusplus.com/facepp/v3/compare' 
    
    data = {'api_key': API_KEY,
            'api_secret': API_SECRET}
    

    files = {'image_file1': (os.path.basename(img_path1), open(img_path1, 'rb'),
            mimetypes.guess_type(img_path1)[0]), 
             'image_file2': (os.path.basename(img_path2), open(img_path2, 'rb'),
            mimetypes.guess_type(img_path2)[0])}
    
    if not detect_face(img_path1) or not detect_face(img_path2):
        raise ValueError('No face detected') 
    
    return requests.post(BASE_URL, files = files, data = data).json()

def run(_id):
    capInput = cv2.VideoCapture(1)
    # avoid blocking
    nextCaptureTime = time.time()
    faces = []
    if not capInput.isOpened(): 
        print('Capture failed because of camera')
        
    start_time = time.time()
    is_saved = False
    while time.time() - start_time < 5:
        ret, img = capInput.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if nextCaptureTime < time.time():
            nextCaptureTime = time.time() + 0.05
            faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) != 0:
            if not is_saved:
                filename = '14081120_'+ str(int(time.time())) + '.jpg'
                cv2.imwrite(filename, img)
                print('image saved')
                is_saved = True
            for x, y, w, h in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), 255, 2)
            cv2.imshow('FaceDetect', img)
        # the ascii of ESC is 27
        if cv2.waitKey(1) & 0xFF == 27: 
            break
    if not is_saved:
        print('Try again!')
        
    capInput.release()
    cv2.destroyAllWindows()

    base_image = os.path.join(settings.MEDIA_ROOT, 'photo', str(_id)+'.jpg')
    print(check(base_image, filename))

def collect():
    capInput = cv2.VideoCapture(0)
    nextCaptureTime = time.time()
    faces = []
    ids = []
    if not capInput.isOpened(): 
        print('Capture failed because of camera')
    while True:
        _id = input('enter student ID:')
        ids.append(_id)
        start_time = time.time()
        file_name = str(_id) + '.jpg' 
        image = None
        while time.time() - start_time < 3:
            ret, img = capInput.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if nextCaptureTime < time.time():
                nextCaptureTime = time.time() + 0.05
                faces = faceCascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) != 0:
                image = img
                for x, y, w, h in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), 255, 2)
                cv2.imshow('FaceDetect', img)
            if cv2.waitKey(1) & 0xFF == 27: 
                break
        if image is not None:
            cv2.imwrite(file_name, image)
        else:
            print('try again')
    capInput.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    
    _id = input('enter student id:')
    run(_id)

    #collect()
    
    
    
    
    