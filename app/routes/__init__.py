from .index import index_route
from .members import members


def register_routes(app):
    app.register_blueprint(index_route)
    app.register_blueprint(members, url_prefix='/members')
