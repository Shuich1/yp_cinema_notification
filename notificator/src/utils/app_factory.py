from flask import Flask

from src.config import Settings
from src.utils.routing import register_endpoints


def create_app(settings: Settings) -> Flask:
    app = Flask(__name__)

    # routing endpoints
    register_endpoints(app)

    app.app_context().push()

    return app
