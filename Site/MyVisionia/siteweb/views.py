# les vues de l'affichage
import aiohttp_jinja2
import json
from aiohttp import web
from aiortc import RTCSessionDescription, RTCPeerConnection
from camera import CamVideoStreamTrack, Expo, Lumino
import configparser

pcs = set()





@aiohttp_jinja2.template('htmldetest.html')
def accueil(request):
    name = request.rel_url.query.get('name', '')
    return {'name': name, 'surname': 'Svetlov'}


async def on_shutdown(app):
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()


async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():

        print("Connection state is %s" % pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)
        
    await pc.setRemoteDescription(offer)
    pc.addTrack(CamVideoStreamTrack())

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )
async def variables (request):
    try:
        Lumino = request.query['light']
        Expo = request.query['exposure']

    except Exception as e :
        return web.Response(text='Nope', status=500)

@aiohttp_jinja2.template('index.html')
async def index(request):
    Expo=5
    Luminom=3

    if request.method == 'POST':
        contenu = await request.post()
        print(contenu)
        # error = validate_json(contenu)
        # if error:
        #     return {'error': error}
        # else:
        #     # login form is valid
        #     location = request.app.router['index'].url_for()
        #     raise web.HTTPFound(location=location)
    #if request.method == POST:
    #    ecrire json

    #lire json
    return {'expo': Expo,'lum':Lumino}

async def index_post(request):
    data = await request.post()
    web.Response(content_type="text/html", text=data)

async def javascript(request):
    content = open("templates/client.js", "r").read()
    return web.Response(content_type="application/javascript", text=content)

async def logo(request):
    content = open("templates/logo.html", "r").read()
    return web.Response(content_type="text/html", text=content)

async def parametrage(request):
    content = open("templates/spintest.html", "r").read()
    return web.Response(content_type="text/html", text=content)

async def options(request):
    return web.Response(text='Page d\'options de l\'application')

async def television(request):
    return web.Response(text='On va tenter')






