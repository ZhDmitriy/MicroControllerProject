""" Инициализация анатомических точек лица с live и static картинки """

import cv2 as cv
import os
import mediapipe as mp
import numpy as np
import random
import time

import yaml
from urllib.request import urlopen

try:
    import serial.tools.list_ports
except ImportError as e:
    import pip
    pip.main(['install', 'pyserial'])



class FacePoints:
    """ Инициализация ключевых точек лица с live или static картинки"""

    def __init__(self, modeReadFacePoint, thickness=1, circle_radius=1):
        """
        :param modeReadFacePoint: live или static mode
        """

        self.modeReadFacePoint = modeReadFacePoint
        self.mpFaceMesh = mp.solutions.face_mesh
        self.mpDraw = mp.solutions.drawing_utils

        with open('/home/dmitriy/PycharmProjects/FaceIDProject/config.yml', 'r') as config_file:
            espConfig = yaml.safe_load(config_file)
            self.CAMERA_URL = espConfig['CAMERA_CONFIG'][0]['CAMERA_URL'][0]
            self.CAMERA_BUFFRER_SIZE=2048

        if self.modeReadFacePoint == "live":

            def sendMessageErrorCameraServer():
                print("""
                    Проверьте корректность работы CAMERA SERVER с ESP32CAM
                """)

            try:
                self.stream = urlopen(self.CAMERA_URL + ":81/stream")
            except Exception as e:
                print(e)
                sendMessageErrorCameraServer()

            self.faceMesh = self.mpFaceMesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)  # по умолчанию работаем только с 1 лицом

        elif self.modeReadFacePoint == "static":

            self.faceMesh = self.mpFaceMesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)
            self.directory = '/home/dmitriy/PycharmProjects/FaceIDProject/imageData'
            self.facePhoto = os.listdir(self.directory)[0]

        elif self.modeReadFacePoint == "checkPort":
            print("Check Port Func Available")

        self.thickness = thickness
        self.circle_radius = circle_radius
        self.draw = self.mpDraw.DrawingSpec(thickness=self.thickness, circle_radius=self.circle_radius)

    def checkArduinoPortESP(self) -> bool:
        """ Проверяем, что порт существует и к нему подключено какое-то устройство """

        def sendMessageUser():
            print("""
                [ERROR] Подключите ESP32CAM, модели CAMERA_MODEL_AI_THINKER в Arduino, к порту '/dev/ttyUSB0' и плату Arduino Uno к порту '/dev/ttyUSB1' ОС Linux
            """)

        ports = list(serial.tools.list_ports.comports())
        print(len(ports))
        if len(ports) == 0:
            sendMessageUser()
            return False
        else:
            stringPorts = ""
            for port in range(len(ports)):
                stringPorts += str(ports[port])
            if '/dev/ttyUSB0' in stringPorts and '/dev/ttyUSB1' in stringPorts:
                return True
            else:
                sendMessageUser()
                return False

    def getFacePoints(self) -> [[list]]:
        """ Получаем ключевые анатомические точки лица """

        faceDataInteration = []

        if self.modeReadFacePoint == "live":

            time.sleep(random.choice([5, 6, 7]))  # задержка перед считыванием лица

            bts = b''
            while True:
                bts += self.stream.read(self.CAMERA_BUFFRER_SIZE)
                jpghead = bts.find(b'\xff\xd8')
                jpgend = bts.find(b'\xff\xd9')
                if jpghead > -1 and jpgend > -1:
                    jpg = bts[jpghead:jpgend + 2]
                    img = cv.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv.IMREAD_UNCHANGED)
                    cv.imshow('img', img)

                    faceLive = []
                    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
                    results = self.faceMesh.process(imgRGB)

                    if results.multi_face_landmarks:
                        for faceLms in results.multi_face_landmarks:
                            self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACEMESH_CONTOURS,
                                                landmark_drawing_spec=self.draw)

                            for id, lm in enumerate(faceLms.landmark):
                                ih, iw, ic = img.shape
                                x, y = int(lm.x * iw), int(lm.y * ih)
                                faceLive.append([x, y])

                    if len(faceLive) != 0:
                        faceDataInteration.append(faceLive)

                if len(faceDataInteration) == 1:
                    return np.array(faceDataInteration)

        elif self.modeReadFacePoint == "static":

            faceStatic = []
            photoClient = cv.imread(f"{self.directory}/{self.facePhoto}")
            image_rgb = cv.cvtColor(photoClient, cv.COLOR_BGR2RGB)
            results = self.faceMesh.process(image_rgb)

            if results.multi_face_landmarks:
                for faceLms in results.multi_face_landmarks:
                    for id, lm in enumerate(faceLms.landmark):
                        ih, iw, ic = photoClient.shape
                        x, y = int(lm.x * iw), int(lm.y * ih)
                        faceStatic.append([x, y])

            if len(faceStatic) != 0:
                faceDataInteration.append(faceStatic)

        return np.array(faceDataInteration)
