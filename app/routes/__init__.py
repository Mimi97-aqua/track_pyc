from .index import index_route


def register_routes(app):
    app.register_blueprint(index_route)
