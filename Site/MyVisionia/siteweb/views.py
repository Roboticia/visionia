# les vues de l'affichage
import aiohttp_jinja2
import json
from aiohttp import web
from aiortc import RTCSessionDescription, RTCPeerConnection
from camera import CamVideoStreamTrack
import configparser
import logging
logging.basicConfig(level=logging.INFO)

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

@aiohttp_jinja2.template('index.html')
async def index(request):
    from camera import Expo, Lumino

    if request.method == 'POST':
        contenu = await request.post()
        logging.info("POST = "+str(contenu))


        with open('sauvegarde.json','r+') as json_file:
            data = json.load(json_file)
            print (data['courant'])
            for p in data['courant']:
                p['exposition']=contenu.getone("Expo", Expo)
                p['lumiere'] = contenu.getone("Lumi", Lumino)
                print(p['exposition'])
                print("lumiere"+str(p['lumiere']))
                print (data)
            json.dump(data, json_file)
            json_file.close()

        with open('sauvegarde.json') as json_file:
            for p in data['courant']:
                Expo = int(p['exposition'])
                Lumino = int(p['lumiere'])
            json_file.close()

    return {'expo': Expo,'lum':Lumino}


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






