#On lance ce fichier pour lancer le seveur

import logging
from aiohttp import web

import os
import aiohttp_jinja2
import jinja2
import cv2
from utils import ArducamUtils
import subprocess


logging.basicConfig(level=logging.DEBUG)

ROOT = os.path.dirname(__file__)
Expo=40
Freeram=50

from camera import allumage

pcs = set()
logging.debug('SET EFFECTUE')

    
if __name__ == "__main__":
    opt=allumage(Expo)
    
    
    app = web.Application()

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates/'))

    from routes import setup_routes
    setup_routes(app)
    web.run_app(app)
