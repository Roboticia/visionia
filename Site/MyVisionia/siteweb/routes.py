#Les chemins
from views import accueil, index, javascript, offer, acquisition


def setup_routes(app):
    app.router.add_get('/', accueil)
    app.router.add_get('/acquisition', acquisition)
    app.router.add_static('/stockage', 'templates/LEdossier')
    app.router.add_get("/video", index)
    app.router.add_post('/video', index)
    app.router.add_get("/client.param.js", javascript)
    app.router.add_post("/offer", offer)


