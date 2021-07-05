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
import time
import configparser


import logging
from av import VideoFrame
from utils import ArducamUtils
from aiohttp import web
from aiortc.contrib.media import MediaPlayer

logging.basicConfig(level=logging.CRITICAL,filename="cam.log", filemode="a", format='%(asctime)s - %(levelname)s - %(message)s')

Expo=1000
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
        self.frames = []
        self.mode=mode
        self.cptImages=0
        self.moduloEcriture=Freeram
    async def recv(self):
        start_time=time.time() #uniquement pour les loggers
        logging.critical('%3f : Debut de cycle',time.time() - start_time)
        ret, frame = cap.read()
        logging.critical('%3f : Lecture de la frame OK', time.time() - start_time)
        frame = arducam_utils.convert(frame)
        logging.critical('%3f : Conversion arducam OK', time.time() - start_time)

        if self.mode == 'usual':
            cv2.imwrite('cam.jpg',frame)
            logging.critical('%3f : Ecriture disque OK', time.time() - start_time)
            img = cv2.imread('cam.jpg')
            logging.critical('%3f : Lecture disque OK', time.time() - start_time)
            """if self.counter%(Freeram)==(0):
                self.frames=[]
                logging.critical('%3f : Liste vide OK', time.time() - start_time)
            self.frames.append(VideoFrame.from_ndarray(numpy.array(img)))
            logging.critical('%3f : Transtypee et envoyee OK', time.time() - start_time)
            pts, time_base = await self.next_timestamp()
            frame = self.frames[self.counter%(Freeram)]
            logging.critical('%3f : Conversion arducam OK', time.time() - start_time)
            logging.debug(self.counter)
            frame.pts = pts
            frame.time_base = time_base
            self.counter += 1
            logging.critical('%3f : Fin de cycle', time.time() - start_time)"""

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
        if self.counter%(Freeram)==(0):
            self.frames=[]
            logging.critical('%3f : Liste vide OK', time.time() - start_time)
        self.frames.append(VideoFrame.from_ndarray(numpy.array(img)))
        logging.critical('%3f : Transtypee et envoyee OK', time.time() - start_time)
        pts, time_base = await self.next_timestamp()
        frame = self.frames[self.counter%(Freeram)]
        logging.critical('%3f : Conversion arducam OK', time.time() - start_time)

        logging.debug(self.counter)
        frame.pts = pts
        frame.time_base = time_base
        self.counter += 1
        logging.critical('%3f : Fin de cycle', time.time() - start_time)
        return frame
