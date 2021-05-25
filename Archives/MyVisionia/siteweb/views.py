#les vues de l'affichage

from aiohttp import web

async def accueil(request):
    content = open("siteweb/templates/htmldetest.html", "r").read()
    return web.Response(content_type="text/html", text=content)
async def marche(request):
    return web.Response(text='Page de mise en marche du capteur')
async def parametrage(request):
    return web.Response(text='Page de paramétrage du capteur')
async def options(request):
    return web.Response(text='Page d\'options de l\'application')
async def camera(request):
    return web.Response(text='On va tenter')





