#Les chemins

from views import accueil, logo, parametrage, options, camera


def setup_routes(app):
    app.router.add_get('/', accueil)
    app.router.add_get('/logo', logo)
    app.router.add_get('/options', options)
    app.router.add_get('/parametrage', parametrage)
    app.router.add_get('/visualisation', camera)
    app.router.add_static('/mincss', 'templates/css')
    app.router.add_static('/style', 'templates/css')

    