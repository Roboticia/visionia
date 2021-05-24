#On lance ce fichier pour lancer le seveur

import logging
from aiohttp import web
import os
import aiohttp_jinja2
import jinja2
import cv2
from utils import ArducamUtils
import subprocess


def allumage(Expo):
    #Init camera
    cmd1 = 'v4l2-ctl -d 0 -c exposure='+str(Expo)
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    arducam_utils = ArducamUtils(0)
    cap.set(cv2.CAP_PROP_CONVERT_RGB, arducam_utils.convert2rgb)
    

    # Aquisition des dimentions de l'image en provenance du capteur
    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    logging.debug('Caméra initialisée')

    # needed to purge the frame with default exposure
    for i in range(6):
        subprocess.call(cmd1, shell=True)
        ret, frame = cap.read()
    logging.debug('Temps d\'exposition réglé\n Allumage effectué')
    return [cmd1,cap]


logging.basicConfig(level=logging.DEBUG)

ROOT = os.path.dirname(__file__)
Expo=40
Freeram=50

pcs = set()
logging.debug('SET EFFECTUE')

if __name__ == "__main__":


    
    opt=allumage(Expo)
    cmd1=opt[0]
    cap=opt[1]
    app = web.Application()

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates/'))

    from routes import setup_routes
    setup_routes(app)
    web.run_app(app)
