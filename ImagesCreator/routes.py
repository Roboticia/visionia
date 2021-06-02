#Les chemins

from views import index, javascript, offer


def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get("/client.js", javascript)
    app.router.add_post("/offer", offer)

    
