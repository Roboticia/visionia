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
logging.basicConfig(level=logging.INFO)

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
    logging.debug('Caméra initialisée')

    # needed to purge the frame with default exposure
    for i in range(6):
        subprocess.call(cmd1, shell=True)
        ret, frame = cap.read()
    logging.debug('Temps d\'exposition réglé\n Allumage effectué')
    

class CamVideoStreamTrack(VideoStreamTrack):


    def __init__(self,mode='display'):
        super().__init__()  # don't forget this!
        self.counter = 0
        self.frames = []
        self.mode=mode
        self.cptImages=0
        self.moduloEcriture=80
    async def recv(self):
        ret, frame = cap.read()
        frame = arducam_utils.convert(frame)


        if self.mode == 'usual':
            cv2.imwrite('cam.jpg',frame)
            img = cv2.imread('cam.jpg')
            if self.counter%(Freeram)==(0):
                self.frames=[]
                logging.debug('Liste videe')
            self.frames.append(VideoFrame.from_ndarray(numpy.array(img)))
            logging.debug('Frame dans la liste')
            pts, time_base = await self.next_timestamp()
            frame = self.frames[self.counter%(Freeram)]
            logging.debug('Frame lue')
            logging.debug(self.counter)
            frame.pts = pts
            frame.time_base = time_base
            self.counter += 1

        if self.mode == 'memory':

            if (self.counter-1)%self.moduloEcriture:
                #cv2.imwrite('test.jpg', frame)
                #img = cv2.imread('test.jpg')
                a= 'images/'+("{:0=6}".format(self.cptImages)) + '.jpg'
                print (a)
                cv2.imwrite((a), frame)
                img = cv2.imread(a)
                self.cptImages+=1

            else:
                cv2.imwrite('cam.jpg', frame)
                img = cv2.imread('cam.jpg')
            if self.counter%(Freeram)==(0):
                self.frames=[]
                logging.debug('Liste videe')
            self.frames.append(VideoFrame.from_ndarray(numpy.array(img)))
            logging.debug('Frame dans la liste')
            pts, time_base = await self.next_timestamp()
            frame = self.frames[self.counter%(Freeram)]
            logging.debug('Frame lue')
            logging.debug(self.counter)
            frame.pts = pts
            frame.time_base = time_base
            self.counter += 1
        return frame
