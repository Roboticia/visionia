#On lance ce fichier pour lancer le seveur
import logging
from aiohttp import web
from routes import setup_routes
import jinja2
import aiohttp_jinja2

#app = web.Application()
##aiohttp_jinja2.setup(app,
##    loader=jinja2.FileSystemLoader('/path/to/templates/folder'))
#setup_routes(app)
#web.run_app(app)

@aiohttp_jinja2.template("index.html")
class HomeHandler(web.View):

    async def get(self):
        return {}

    async def post(self):
        form = await self.request.post()
        return {"name":form['name']}


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    app = web.Application()
    # setup jinja2 
    aiohttp_jinja2.setup(app,
        loader=jinja2.FileSystemLoader(
            'siteweb/templates'
            ))

    #setup_routes(app)

    app.router.add_get('/test', HomeHandler,name="index")
    app.router.add_post('/', HomeHandler)


    web.run_app(app)