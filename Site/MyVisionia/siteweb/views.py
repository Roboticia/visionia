# les vues de l'affichage
import aiohttp_jinja2
import json
from aiohttp import web
from aiortc import RTCSessionDescription, RTCPeerConnection
from camera import CamVideoStreamTrack
import configparser
import logging
import asyncio

logging.basicConfig(level=logging.INFO)

pcs = set()


@aiohttp_jinja2.template('accueil.html')
def accueil(request):
    name = request.rel_url.query.get('name', '')
    return {'name': name, 'surname': 'Svetlov'}


@aiohttp_jinja2.template('acquisition.html')
async def acquisition(request):
    return {}


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
    mode = params["mode"]
    logging.info(str(mode)+ ' mode')

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():

        print("Connection state is %s" % pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    await pc.setRemoteDescription(offer)



    if (mode == 'usual'):
        pc.addTrack(CamVideoStreamTrack(mode='usual'))
    if (mode == 'memory'):
        pc.addTrack(CamVideoStreamTrack(mode='memory'))


    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )


@aiohttp_jinja2.template('param.html')
async def index(request):
    from camera import Expo, Lumino, allumage

    if request.method == 'POST':
        contenu = await request.post()
        logging.info("POST = " + str(contenu))

        with open('sauvegarde.json', 'r') as json_file:
            data = json.load(json_file)
        print(data['courant'])
        for p in data['courant']:
            p['exposition'] = contenu.getone("Expo", Expo)
            p['lumiere'] = contenu.getone("Lumi", Lumino)
            print(p['exposition'])
            print("lumiere" + str(p['lumiere']))
            print(data)

        json_file.close()

        with open('sauvegarde.json', 'w') as json_file:
            json.dump(data, json_file)
        json_file.close()

        with open('sauvegarde.json') as json_file:
            data = json.load(json_file)
            for p in data['courant']:
                Expo = int(p['exposition'])
                Lumino = int(p['lumiere'])
                Freeram = int(p['taillecycle'])
            json_file.close()
        allumage(Expo)

    return {'expo': Expo, 'lum': Lumino}


async def javascriptparam(request):
    content = open("templates/client.param.js", "r").read()
    return web.Response(content_type="application/javascript", text=content)

async def javascriptacquisition(request):
    content = open("templates/client.acquisition.js", "r").read()
    return web.Response(content_type="application/javascript", text=content)

@aiohttp_jinja2.template('memoire.html')
async def memoire(request):
    return {}

async def handle_404(request):
    return aiohttp_jinja2.render_template('erreur.html', request, {}, status=404)



