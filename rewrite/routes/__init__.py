from .base_routes import base_routes


def register_routes(app):
    app.register_blueprint(base_routes)
