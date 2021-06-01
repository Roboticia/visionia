#On lance ce fichier pour lancer le seveur

import logging
from aiohttp import web

import os
import aiohttp_jinja2
import jinja2
import cv2

import subprocess


logging.basicConfig(level=logging.DEBUG)

ROOT = os.path.dirname(__file__)

from camera import allumage


logging.debug('SET EFFECTUE')

    
if __name__ == "__main__":
    allumage()
    
    
    app = web.Application()

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates/'))

    from routes import setup_routes
    setup_routes(app)
    web.run_app(app)
