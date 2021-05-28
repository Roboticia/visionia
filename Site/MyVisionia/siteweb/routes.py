#Les chemins

from views import accueil, logo, parametrage, options, television, index, javascript, offer,television


def setup_routes(app):
    app.router.add_get('/', accueil)
    app.router.add_get('/logo', logo)
    app.router.add_get('/options', options)
    app.router.add_get('/parametrage', parametrage)
    app.router.add_get('/visualisation', television)
    app.router.add_static('/stockage', 'templates/LEdossier')
    app.router.add_get("/video", index(15))
    app.router.add_get("/client.js", javascript)
    app.router.add_post("/offer", offer)
    
