#les vues de l'affichage
import aiohttp_jinja2
import json
from aiohttp import web
from aiortc import RTCSessionDescription, RTCPeerConnection
from camera import CamVideoStreamTrack

pcs = set()
@aiohttp_jinja2.template('htmldetest.html')
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
def index(request):
    from camera import Expo, Cptimages
    return {'expo': Expo,'Nbimages':Cptimages}
async def javascript(request):
    content = open("templates/client.js", "r").read()
    return web.Response(content_type="application/javascript", text=content)









