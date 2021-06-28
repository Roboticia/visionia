import logging
from aiohttp import web
import os
import aiohttp_jinja2
import jinja2
import cv2
from camera import allumage, Expo
import subprocess
from routes import setup_routes
from middlewares import setup_middlewares



logging.basicConfig(level=logging.DEBUG)
#print(logging.root.level)
ROOT = os.path.dirname(__file__)


logging.basicConfig(level=logging.DEBUG)
print(logging.root.level)

logging.debug('SET EFFECTUE')

app = web.Application()

setup_routes(app)
setup_middlewares(app)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates/'))
allumage(Expo)

if __name__ == "__main__":
    web.run_app(app)


