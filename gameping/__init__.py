from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.absolute()))
# We need to add the child paths to the project! This is so BS...

from gameping.config.settings import settings
db_config = settings["db"]

db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates")

    # app.debug = False
    app.config["SQLALCHEMY_DATABASE_URI"] = f"{db_config['database']}{db_config['engine']}" \
                                            f"://{db_config['username']}:{db_config['password']}" \
                                            f"@{db_config['address']}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    from gameping.web.views import web_blueprint as main_blueprint
    app.register_blueprint(main_blueprint)

    db.init_app(app)

    return app
