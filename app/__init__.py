import os

from flask import Flask

from app import db, fiado


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config["DATABASE"] = os.path.join(app.instance_path, "fiabar.db")
    if test_config:
        app.config.update(test_config)
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    app.register_blueprint(fiado.bp)
    return app
