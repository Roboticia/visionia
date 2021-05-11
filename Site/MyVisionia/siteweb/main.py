#On lance ce fichier pour lancer le seveur
import logging
from aiohttp import web
from routes import setup_routes

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    app = web.Application()
    setup_routes(app)
    web.run_app(app)