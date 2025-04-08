from flask import Flask
from app.config import getsettings


def create_app():
    app = Flask(__name__)
    app.config.from_object(getsettings())
    return app


app = create_app()

from app import views, models
