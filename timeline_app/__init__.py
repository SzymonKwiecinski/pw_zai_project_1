import os
from flask import Flask
from dotenv import load_dotenv
from timeline_app import models
from timeline_app.database import db
from timeline_app.routes import pages


def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config["POSTGRES_URL"] = os.environ.get("POSTGRES_URL")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("POSTGRES_URL")
    db.init_app(app)
    app.register_blueprint(pages)
    #
    with app.app_context():
        # db.drop_all()
        db.create_all()

    return app
