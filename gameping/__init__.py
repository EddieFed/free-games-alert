# System library imports
import os

# External library imports
from flask import Flask

# Local library imports
from gameping.database import db


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=False)

    # If config exists, use it!
    app.config.from_object('config.DevelopmentConfig')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass  # lmao

    db.init_app(app)

    # Assign decoupled routes to the app!
    from gameping.web import views
    app.register_blueprint(views.bp)

    return app


