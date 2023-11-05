import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_uploads import IMAGES, UploadSet, configure_uploads
from sqlalchemy import text

from timeline_app.database import db
from timeline_app.routes import pages

photos = UploadSet("photos", IMAGES)
UPLOAD_FOLDER = "timeline_app/static/img"
QUERIES_DIR = Path(__file__).parent / "queries"


def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config["POSTGRES_URL"] = os.environ.get("POSTGRES_URL")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("POSTGRES_URL")
    app.config["UPLOADED_PHOTOS_DEST"] = UPLOAD_FOLDER
    app.photos = photos
    configure_uploads(app, app.photos)

    db.init_app(app)
    app.register_blueprint(pages)

    #
    with app.app_context():
        db.drop_all()
        db.create_all()

        populate_tables = QUERIES_DIR / "populate_tables.sql"
        db.session.execute(text(populate_tables.read_text()))
        db.session.commit()

    return app
