from .base_routes import base_routes
from .autopilot_routes import autopilot_routes


def register_routes(app):
    app.register_blueprint(base_routes)
    app.register_blueprint(autopilot_routes)
