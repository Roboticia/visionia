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


import logging
from av import VideoFrame
from utils import ArducamUtils
from aiohttp import web

from aiortc.contrib.media import MediaPlayer

Expo=40
Freeram=50
Ecriture=0
Secentrimages=2
Cptimages=0
Moduloecriture=Expo/Secentrimages


cmd1 = 'v4l2-ctl -d 0 -c exposure='+str(Expo)
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
arducam_utils = ArducamUtils(0)
w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
logging.debug('Declaration des variables OK')

def allumage():
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

    def __init__(self):
        super().__init__()  # don't forget this!
        self.counter = 0
        self.frames = []


    async def recv(self):
        ret, frame = cap.read()
        frame = arducam_utils.convert(frame)
        cv2.imwrite('cam.jpg',frame)
        if Ecriture % Moduloecriture==0 :
            cv2.imwrite('../Documents/test/cam' + ("{:0=4}".format(Cptimages)) + '.jpg', frame)
            Cptimages+=1
        Ecriture+=1
        cv2.imwrite('cam.jpg')
        img = cv2.imread('cam.jpg')
        if self.counter%(Freeram)==(0):
            self.frames=[]
            logging.debug('Liste vidée')
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
