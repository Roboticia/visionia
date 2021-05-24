from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
import argparse
import asyncio
import json
import os#a faire sauter
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
from main import cap

from aiortc.contrib.media import MediaPlayer

class CamVideoStreamTrack(VideoStreamTrack):


    def __init__(self):
        super().__init__()  # don't forget this!
        self.counter = 0
        self.frames = []

    async def recv(self):
        ret, frame = cap.read()
        frame = arducam_utils.convert(frame)
        cv2.imwrite('cam.jpg',frame)

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
