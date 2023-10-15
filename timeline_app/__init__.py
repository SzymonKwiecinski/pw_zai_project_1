import os
from flask import Flask
from dotenv import load_dotenv
from pymongo import MongoClient

from timeline_app.routes import pages

load_dotenv()

MONGODB_URI = os.environ.get("MONGODB_URI")
SECRET_KEY = os.environ.get("SECRET_KEY", "111111111111")


def create_app():
    app = Flask(__name__)
    app.config["MONGODB_URI"] = MONGODB_URI
    app.config["SECRET_KEY"] = SECRET_KEY
    app.db = MongoClient(MONGODB_URI).get_default_database()

    app.register_blueprint(pages)
    return app
