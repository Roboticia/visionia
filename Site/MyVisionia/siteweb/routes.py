#Les chemins
from views import accueil, index, javascriptacquisition, javascriptparam, offer, acquisition, memoire


def setup_routes(app):
    app.router.add_get('/', accueil)
    app.router.add_get('/acquisition', acquisition)
    app.router.add_static('/stockage', 'templates/LEdossier')
    app.router.add_get("/video", index)
    app.router.add_post('/video', index)
    app.router.add_get("/client.param.js", javascriptparam)
    app.router.add_get("/client.acquisition.js", javascriptacquisition)
    app.router.add_post("/offer", offer)
    app.router.add_get("/memoire", memoire)



