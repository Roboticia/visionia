#Les chemins

from views import accueil, marche, parametrage, options, camera


def setup_routes(app):
    app.router.add_get('/', accueil)
    app.router.add_get('/marchenormale', marche)
    app.router.add_get('/options', options)
    app.router.add_get('/parametrage', parametrage)
    app.router.add_get('/visualisation', camera)

    