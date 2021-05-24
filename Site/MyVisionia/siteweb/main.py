#On lance ce fichier pour lancer le seveur

import logging
from aiohttp import web
from routes import setup_routes
import aiohttp_jinja2
import jinja2

from camera import *


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


    setup_routes(app)
    web.run_app(app)
