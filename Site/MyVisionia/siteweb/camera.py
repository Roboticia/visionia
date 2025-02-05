from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
import argparse
import asyncio
import json
import platform
import ssl
import math
import cv2
import numpy
import subprocess
import settings
import time
import configparser


import logging
from av import VideoFrame

from Site.MyVisionia.siteweb.darknet.darknet_image import *
from utils import ArducamUtils
from aiohttp import web
from aiortc.contrib.media import MediaPlayer

logging.basicConfig(level=logging.CRITICAL)

Expo=100
Lumino=50
Freeram=50

with open('sauvegarde.json') as json_file:
    data = json.load(json_file)
    for p in data['courant']:
        Expo = int(p['exposition'])
        Lumino = int(p['lumiere'])
        Freeram = int(p['taillecycle'])
    json_file.close()

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
arducam_utils = ArducamUtils(0)
for key, values in settings.DARKNET_CONF.items():
    weights = values['WEIGHT_PATH']
    config_file = values['CFG']
    data_file = values['DATA']
    batch_size = values['BATCH']
    width = values['WIDTH']
    height = values['HEIGHT']

    'HEIGHT': 416,

network, class_names, class_colors = darknet.load_network(
        config_file,
        data_file,
        weights,
        batch_size
    )


def allumage(Expo):

    cmd1 = 'v4l2-ctl -d 0 -c exposure='+str(Expo)
    print (Expo)
    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    logging.debug('Declaration des variables OK')
    #Init camera
    cap.set(cv2.CAP_PROP_CONVERT_RGB, arducam_utils.convert2rgb)
    # Aquisition des dimentions de l'image en provenance du capteur
    logging.debug('Camera initialisee')

    # needed to purge the frame with default exposure
    for i in range(6):
        subprocess.call(cmd1, shell=True)
        ret, frame = cap.read()
    logging.debug('Temps d\'exposition regle\n Allumage effectue')
    

class CamVideoStreamTrack(VideoStreamTrack):


    def __init__(self,mode='display'):

        super().__init__()  # don't forget this!
        self.counter = 0
        self.frame = VideoFrame
        self.mode=mode
        self.cptImages=0
        self.moduloEcriture=Freeram

    # traitement opencv
    async def recv(self):

        start_time=time.time() #uniquement pour les loggers
        logging.critical('%3f : Debut de cycle',time.time() - start_time)
        ret, frame = cap.read()
        frame = arducam_utils.convert(frame)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (width, height),
                                   interpolation=cv2.INTER_LINEAR)
        img_for_detect = darknet.make_image(width, height, 3)
        darknet.copy_image_from_bytes(img_for_detect, frame_resized.tobytes())
        #print(type(frame))
        logging.critical('%3f : Lecture de la frame OK', time.time() - start_time)
#        frame = arducam_utils.convert(frame)
        frame, _ = image_detection(img_for_detect, network, class_names, class_colors, thresh=0.3)

        # img = frame
        logging.critical('%3f : Conversion arducam OK', time.time() - start_time)

        if self.mode == 'usual':
            img = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            #img = cv2.line(img, (0, 0), (150, 150), (255, 0, 0), 10)
            logging.critical('%3f : Changement de numpy array', time.time() - start_time)

        if self.mode == 'memory':

            if (self.counter-1)%self.moduloEcriture:
                a= 'images/'+("{:0=6}".format(self.cptImages)) + '.jpg'
                logging.critical('image ecrite sous le nom : %s',a)
                cv2.imwrite((a), frame)
                logging.critical('%3f : Ecriture disque OK', time.time() - start_time)
                img = cv2.imread(a)
                logging.critical('%3f : Lecture disque OK', time.time() - start_time)
                self.cptImages+=1

            else:
                cv2.imwrite('cam.jpg', frame)
                logging.critical('%3f : Ecriture disque OK', time.time() - start_time)
                img = cv2.imread('cam.jpg')
                logging.critical('%3f : Lecture disque OK', time.time() - start_time)

        self.frame = VideoFrame.from_ndarray(numpy.array(img))
        logging.critical('%3f : Transtypee et envoyee OK', time.time() - start_time)
        pts, time_base = await self.next_timestamp()
        frame = self.frame
        logging.critical('%3f : Conversion arducam OK', time.time() - start_time)
        frame.pts = pts
        frame.time_base = time_base
        self.counter += 1
        logging.critical('%3f : Fin de cycle', time.time() - start_time)
        return frame
