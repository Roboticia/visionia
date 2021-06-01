#Les chemins

from views import accueil, logo, parametrage, options, television, index, javascript, offer,television


def setup_routes(app):
    app.router.add_get('/', index)

    
