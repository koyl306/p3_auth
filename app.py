from flask import Flask
from dotenv import load_dotenv

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from database import db

from auth import auth
from admin import admin

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# RATE LIMITER
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[]
)

with app.app_context():
    db.create_all()

app.register_blueprint(auth, url_prefix="/auth")

app.register_blueprint(admin, url_prefix="/admin")

if __name__ == "__main__":
    app.run(debug=True)