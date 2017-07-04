# -*- coding: utf-8 -*-
"""
Created on Sat Jul 01 09:57:14 2017

@author: wanggd
"""

import os
import cv2
import time
from api import get_response, faceCascade
import threading
import winsound
import requests
from tkinter import *

face_base = 'data'
face_db = os.path.join(face_base, 'face_db')
face_var = os.path.join(face_base, 'face_var')
SERVER_BASE = 'http://localhost:8000'
# SERVER_BASE = 'http://uranus.kahsolt.tk'
SERVER_URL = SERVER_BASE + '/student/attendance'
STATE_URL = SERVER_BASE + '/teacher/attendance_view'
ID = None
INTERVAL = 10

cv2.namedWindow('FaceDetect', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('FaceDetect', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


def check(img_path1, img_path2):
    response = get_response(img_path1, img_path2)
    # print(response)
    return response['confidence'] > 80


def draw_tick(img):
    point1 = (int(img.shape[0] / 3), int(img.shape[1] / 2))
    point2 = (int(2 * img.shape[0] / 3), int(2 * img.shape[1] / 3))
    point3 = (int(img.shape[0]), int(img.shape[1] / 6))
    cv2.line(img, point1, point2, (0, 255, 0), 8)
    cv2.line(img, point2, point3, (0, 255, 0), 8)


def draw_cross(img):
    point1 = (int(img.shape[0] / 2), int(img.shape[1] / 4))
    point2 = (int(img.shape[0]), int(2 * img.shape[1] / 3))
    point3 = (int(img.shape[0]), int(img.shape[1] / 4))
    point4 = (int(img.shape[0] / 2), int(2 * img.shape[1] / 3))
    cv2.line(img, point1, point2, (0, 0, 255), 8)
    cv2.line(img, point3, point4, (0, 0, 255), 8)


def search_webcam():
    i = 0
    while True:
        capInput = cv2.VideoCapture(i).isOpened()
        if capInput:
            return i
        i += 1


def send(user_id):
    requests.get(SERVER_URL, params={'id': user_id})


def read_state():
    try:
        STATE = int(requests.get(STATE_URL, params={'action': 4}).text)
    except:
        print('Server crashed')
    print(STATE)
    return STATE


def collect():
    STATE = 2
    collect_start = time.time()
    nextCaptureTime = time.time()
    faces = []
    global ID
    image = None
    face_image = None
    if not capInput.isOpened():
        print('Capture failed because of camera')

    while STATE == 2:
        if time.time() - collect_start > INTERVAL:
            collect_start = time.time()
            STATE = read_state()
            if STATE != 2:
                break
        if ID is not None:
            face_image = str(ID) + '.jpg'
            image = None
        ret, img = capInput.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if nextCaptureTime < time.time():
            nextCaptureTime = time.time() + 0.05
            faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) != 0:
            image = img.copy()
            for x, y, w, h in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), 255, 2)
        cv2.imshow('FaceDetect', img)
        if cv2.waitKey(1) & 0xFF == 27:
            break
        if image is not None and ID is not None and face_image is not None:
            cv2.imwrite(os.path.join(face_db, face_image), image)
            draw_tick(image)
            begin = time.time()
            while time.time() - begin < 1:
                cv2.imshow('FaceDetect', image)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
            winsound.Beep(440, 1000)
            image = None
            ID = None
            face_image = None
    # capInput.release()
    # cv2.destroyAllWindows()
    return STATE


def wait_for_input():
    global ID
    while True:
        ID = input('enter student id:')


def run():
    STATE = 0
    attend_start = time.time()

    global ID

    if not capInput.isOpened():
        print('Capture failed because of camera')
    # threading.Thread(target=wait_for_input).start()

    # Note: we have to place these variable like
    # "faces" and "nextCaptureTime" outside while loop to
    # avoid allocating and releasing memory for efficiency
    nextCaptureTime = time.time()
    faces = []
    is_saved = False
    face_image = None

    while STATE == 0:
        if time.time() - attend_start > INTERVAL:
            attend_start = time.time()
            STATE = read_state()
            if STATE == 1:
                break
        is_saved = False
        # avoid blocking
        face_image = None
        nextCaptureTime = time.time()
        ret, img = capInput.read()
        if nextCaptureTime < time.time():
            nextCaptureTime = time.time() + 0.05
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) != 0:
            if not is_saved and ID is not None:
                face_image = str(ID) + '_' + str(int(time.time())) + '.jpg'
                face_image = os.path.join(face_var, face_image)
                cv2.imwrite(face_image, img)
                is_saved = True
            else:
                for x, y, w, h in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), 255, 2)
        cv2.imshow('FaceDetect', img)
        if cv2.waitKey(1) & 0xFF == 27:
            break

        if is_saved:
            base_image = os.path.join(face_db, str(ID) + '.jpg')
            if check(base_image, face_image):
                draw_tick(img)
                begin = time.time()
                while time.time() - begin < 1:
                    cv2.imshow('FaceDetect', img)
                    if cv2.waitKey(1) & 0xFF == 27:
                        break
                send(ID)
                winsound.Beep(440, 1000)
                ID = None
                print(ID)
                is_saved = False
            else:
                ID = None
                is_saved = False
                winsound.Beep(440, 1000)
                draw_cross(img)
                begin = time.time()
                while time.time() - begin < 1:
                    cv2.imshow('FaceDetect', img)
                    if cv2.waitKey(1) & 0xFF == 27:
                        break

    # capInput.release()
    # cv2.destroyAllWindows()
    return STATE


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        # self.bind("<Enter>", self.sign_in)

    def createWidgets(self):
        self.labelInfo = Label(self, text='请输入学号：')
        self.labelInfo.pack(fill=BOTH)
        self.nameInput = Entry(self)
        self.nameInput.pack(fill=BOTH)
        self.alertButton = Button(self, text='确定', command=self.sign_in)
        self.alertButton.pack(fill=BOTH)

    def sign_in(self):
        global ID
        temp = self.nameInput.get()
        if temp != '':
            ID = temp
            print(ID)
        self.nameInput.delete('0', 'end')
        # messagebox.showinfo('Message', 'Hello, %s' % name)


def normal(STATE):
    start_time = time.time()
    while STATE != 2 and STATE != 0:
        if time.time() - start_time > INTERVAL:
            start_time = time.time()
            STATE = read_state()
        ret, img = capInput.read()
        cv2.imshow('FaceDetect', img)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    return STATE


def start():
    STATE = read_state()
    while True:
        if STATE == 2:
            STATE = collect()
        elif STATE == 0:
            STATE = run()
        else:
            STATE = normal(STATE)


def initTk(tk):
    WINWIDTH = 1366
    WIDTH = 150;
    HEIGHT = 75
    X = WINWIDTH / 2 - WIDTH / 2;
    Y = 5
    tk.minsize(WIDTH, HEIGHT)
    tk.maxsize(WIDTH, HEIGHT)
    tk.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, X, Y))
    tk.wm_attributes('-topmost', 1)  # 窗口置顶，仅win有效……


# Main Entry
capInput = cv2.VideoCapture(search_webcam())
tk = Tk()
initTk(tk)
app = Application(tk)
app.master.title('签到系统')
threading.Thread(target=start).start()
app.mainloop()

