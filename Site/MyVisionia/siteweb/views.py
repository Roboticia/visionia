#les vues de l'affichage
import jinja2
import aiohttp_jinja2
from aiohttp import web

@aiohttp_jinja2.template('tmpl.jinja2')
def handler(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}



async def accueil(request):
    content = open("templates/htmldetest.html", "r").read()
    return web.Response(content_type="text/html", text=content)
async def logo(request):
    content = open("templates/logo.html", "r").read()
    return web.Response(content_type="text/html", text=content)
async def parametrage(request):
    return web.Response(text='Page de paramétrage du capteur')
async def options(request):
    return web.Response(text='Page d\'options de l\'application')
async def camera(request):
    return web.Response(text='On va tenter')






